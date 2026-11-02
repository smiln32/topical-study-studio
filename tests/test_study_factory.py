import contextlib
import io
import json
import tempfile
import unittest
from unittest import mock
import threading
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

import study_factory
from study_studio import Handler

ROOT = Path(__file__).resolve().parents[1]


class PlannerFactoryTests(unittest.TestCase):
    def load_example(self):
        return json.loads((ROOT / "shared" / "examples" / "basic" / "spec.json").read_text(encoding="utf-8-sig"))

    def test_example_has_no_validation_findings(self):
        self.assertEqual(study_factory.validate(self.load_example()), [])

    def test_render_uses_exact_letter_canvas_and_page_count(self):
        spec = self.load_example()
        html = study_factory.render(spec)
        self.assertIn("width:816px;height:1056px", html)
        self.assertEqual(html.count('data-document-role="page"'), len(spec["pages"]))

    def test_duplicate_concepts_are_errors(self):
        spec = self.load_example()
        spec["pages"][0]["concept"] = "Daily focus"
        spec["pages"][1]["concept"] = "Daily focus"
        findings = study_factory.validate(spec)
        self.assertTrue(any("repeat the same concept" in finding for finding in findings))

    def test_overlapping_blocks_are_errors(self):
        spec = self.load_example()
        spec["pages"][0]["blocks"][1].update(x=28, y=104, w=300, h=200)
        findings = study_factory.validate(spec)
        self.assertTrue(any("overlap" in finding for finding in findings))

    def test_string_coordinates_do_not_crash_the_overlap_check(self):
        spec = self.load_example()
        spec["pages"][0]["blocks"][0].update(x="28", y=104, w=300, h=200)
        spec["pages"][0]["blocks"][1].update(x=28, y=104, w=300, h=200)
        findings = study_factory.validate(spec)
        self.assertTrue(any("overlap" in finding for finding in findings))

    def test_unknown_content_type_is_an_error(self):
        spec = self.load_example()
        spec["pages"][0]["blocks"][0]["content"] = {"type": "nope"}
        findings = study_factory.validate(spec)
        self.assertTrue(any("unknown content type 'nope'" in finding for finding in findings))

    def test_non_numeric_counts_are_errors(self):
        for content in (
            {"type": "lines", "rows": "abc"},
            {"type": "checklist", "items": ["a"], "blank_rows": None},
            {"type": "choices", "options": ["a"], "lines_after": -1},
            {"type": "split", "left": {"type": "lines", "rows": "x"}},
        ):
            with self.subTest(content=content):
                spec = self.load_example()
                spec["pages"][0]["blocks"][0]["content"] = content
                self.assertTrue(any("must be a whole number" in f for f in study_factory.validate(spec)))

    def test_table_columns_must_be_objects(self):
        spec = self.load_example()
        spec["pages"][0]["blocks"][0]["content"] = {"type": "table", "columns": ["Day", "Notes"]}
        self.assertTrue(any('"columns" must be a list of objects' in f for f in study_factory.validate(spec)))

    def test_malformed_specification_shapes_are_errors_not_crashes(self):
        for spec in (
            [],
            {"pages": {}},
            {"pages": [["not", "a", "page"]]},
            {"pages": [{"title": "T", "blocks": None}]},
            {"pages": [{"title": "T", "blocks": ["not a block"]}]},
            {"pages": [{"title": "T", "blocks": [{"x": 28, "y": 104, "w": 760, "h": 900, "content": "lines"}]}]},
        ):
            with self.subTest(spec=spec):
                findings = study_factory.validate(spec)
                self.assertTrue(findings and all(f.startswith("ERROR") for f in findings))

    def test_main_reports_an_unexpected_failure_plainly(self):
        spec = self.load_example()
        with tempfile.TemporaryDirectory() as tmp:
            spec_path = Path(tmp) / "spec.json"
            spec_path.write_text(json.dumps(spec), encoding="utf-8")
            argv = ["study_factory.py", str(spec_path), str(Path(tmp) / "out.html")]
            with mock.patch("sys.argv", argv), mock.patch.object(study_factory, "render", side_effect=RuntimeError("boom")):
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr):
                    code = study_factory.main()
        self.assertEqual(code, 2)
        self.assertIn("Could not generate: boom", stderr.getvalue())
        self.assertNotIn("Traceback", stderr.getvalue())

    def test_theme_must_be_a_colour(self):
        for theme in ("red; display:none", "#fff\" onload=\"x", "url(javascript:evil)", 7):
            with self.subTest(theme=theme):
                spec = self.load_example()
                spec["pages"][0]["theme"] = theme
                self.assertTrue(any("is not a colour" in f for f in study_factory.validate(spec)))
        for theme in ("#b2c6b1", "#FFF", "rebeccapurple", "rgb(10, 20, 30)"):
            with self.subTest(theme=theme):
                spec = self.load_example()
                spec["pages"][0]["theme"] = theme
                self.assertEqual(study_factory.validate(spec), [])

    def test_table_column_width_must_be_a_length(self):
        spec = self.load_example()
        table = spec["pages"][1]["blocks"][0]["content"]
        table["columns"][0]["width"] = "15%; display:none"
        self.assertTrue(any("is not a length" in f for f in study_factory.validate(spec)))
        table["columns"][0]["width"] = "15%"
        self.assertEqual(study_factory.validate(spec), [])

    def test_content_taller_than_its_box_is_a_warning(self):
        spec = self.load_example()
        block = spec["pages"][0]["blocks"][1]
        block["content"] = {"type": "checklist", "items": [f"Checklist item {i}" for i in range(1, 31)]}
        block["h"] = 200
        findings = study_factory.validate(spec)
        self.assertTrue(any("will not print" in f and "Basic care" in f for f in findings))
        self.assertFalse(any(f.startswith("ERROR") for f in findings))

    def test_long_titles_are_a_warning(self):
        spec = self.load_example()
        spec["pages"][0]["title"] = "A very long page title that keeps going " * 4
        self.assertTrue(any("hides the rest" in f for f in study_factory.validate(spec)))

    def test_invalid_geometry_is_an_error(self):
        cases = [
            {"x": 28, "y": 104, "w": 179, "h": 200},
            {"x": 27, "y": 104, "w": 760, "h": 200},
            {"x": 28, "y": 103, "w": 760, "h": 200},
            {"x": 28, "y": 104, "w": 760, "h": 927},
            {"x": "bad", "y": 104, "w": 760, "h": 200},
        ]
        for geometry in cases:
            with self.subTest(geometry=geometry):
                spec = self.load_example()
                spec["pages"][0]["blocks"] = [{**geometry, "content": {"type": "lines"}}]
                self.assertTrue(any(finding.startswith("ERROR:") for finding in study_factory.validate(spec)))

    def test_titles_and_prompts_are_checked_independently(self):
        spec = self.load_example()
        first, second = spec["pages"][0]["blocks"][:2]
        first["title"] = second["title"] = "Repeated section"
        first["content"]["prompt"] = "First unique prompt"
        second["content"]["prompt"] = "Second unique prompt"
        findings = study_factory.validate(spec)
        self.assertTrue(any("repeats section title" in finding for finding in findings))

        second["title"] = "Unique section"
        second["content"]["prompt"] = "First unique prompt"
        findings = study_factory.validate(spec)
        self.assertTrue(any("repeats prompt" in finding for finding in findings))

    def test_rendered_output_is_substantial_html(self):
        html = study_factory.render(self.load_example())
        self.assertTrue(html.startswith("<!doctype html>"))
        self.assertGreater(len(html), 1000)

    def test_starter_spec_is_valid_and_topic_aware(self):
        spec = study_factory.starter_spec("Morning Routine")
        self.assertEqual(study_factory.validate(spec), [])
        self.assertIn("Morning Routine", spec["set_title"])
        self.assertEqual(len(spec["pages"]), 1)

    def test_version_is_semantic(self):
        self.assertRegex(study_factory.VERSION, r"^\d+\.\d+\.\d+$")


    def test_studio_assets_are_linked_and_encoding_is_clean(self):
        html = (ROOT / "studio" / "index.html").read_text(encoding="utf-8")
        script = (ROOT / "studio" / "app.js").read_text(encoding="utf-8")
        styles = (ROOT / "studio" / "styles.css").read_text(encoding="utf-8")
        self.assertIn('src="app.js?', html)
        self.assertIn('href="styles.css?', html)
        self.assertIn("function editLive", script)
        self.assertIn("function syncInspector", script)
        self.assertIn("function bindPanelSplitter", script)
        self.assertIn('id="leftSplitter"', html)
        self.assertIn('id="rightSplitter"', html)
        self.assertIn("@media(max-width:680px)", styles)
        for text in (html, script, styles):
            self.assertNotIn("\ufffd", text)
            self.assertNotIn("\u00c3", text)
            self.assertNotIn("\u00e2\u20ac", text)

    def test_studio_templates_escape_theme_colour_and_geometry(self):
        script = (ROOT / "studio" / "app.js").read_text(encoding="utf-8")
        for raw in ("${p.theme}", "${b.color}", "${b.x}", "${b.y}", "${b.w}", "${b.h}"):
            self.assertNotIn(raw, script, f"{raw} is interpolated into HTML without esc()")
        self.assertIn("style.setProperty('--theme',p.theme)", script)

    def test_rendered_titles_are_clamped_to_the_header(self):
        html = study_factory.render(self.load_example())
        self.assertIn("-webkit-line-clamp:2", html)
    def test_studio_health_endpoint(self):
        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{server.server_port}/api/health") as response:
                payload = json.loads(response.read())
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["version"], study_factory.VERSION)
            self.assertEqual(response.headers["Cache-Control"], "no-store, max-age=0")
        finally:
            server.shutdown()
            server.server_close()
if __name__ == "__main__":
    unittest.main()
