"""The passage block: what the validator holds, what the page prints, what the starter writes.

Every verse here is placeholder text. No Scripture is kept in this repository.
"""
import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))

import study_factory  # noqa: E402
from test_print_fit import browser, measure  # noqa: E402

NOTICE = "Placeholder for the publisher's notice."


def verses(n, words=12):
    return [{"number": k, "text": " ".join(["placeholder"] * words)} for k in range(1, n + 1)]


def passage(**extra):
    content = {"type": "passage", "reference": "Book 1:1-3", "verses": verses(3), "notice": NOTICE}
    content.update(extra)
    return content


def page_with(content, h=926, w=760):
    return {"pages": [{"concept": "x", "title": "x", "blocks": [{"x": 28, "y": 104, "w": w, "h": h, "title": "Read", "content": content}]}]}


def errors(spec):
    return [f for f in study_factory.validate(spec) if f.startswith("ERROR")]


class PassageValidationTests(unittest.TestCase):
    def test_a_good_passage_has_no_findings(self):
        self.assertEqual(study_factory.validate(page_with(passage())), [])

    def test_missing_reference_verses_number_or_text_are_errors(self):
        for bad in ({"reference": " "}, {"verses": []}, {"verses": "text"}, {"verses": [{"text": "x"}]},
                    {"verses": [{"number": 1, "text": " "}]}, {"verses": [{"number": 0, "text": "x"}]},
                    {"verses": [{"number": True, "text": "x"}]}, {"verses": ["x"]}, {"notice": 5}):
            with self.subTest(bad=bad):
                spec = page_with(passage(**bad))
                self.assertTrue(errors(spec))
                study_factory.estimate_content_height(spec["pages"][0]["blocks"][0]["content"], 760)

    def test_no_notice_draws_a_warning_and_one_notice_satisfies_it(self):
        spec = page_with(passage(notice=""))
        self.assertTrue(any("no copyright notice" in f for f in study_factory.validate(spec)))
        spec["pages"].append({"concept": "y", "title": "y", "blocks": [
            {"x": 28, "y": 104, "w": 760, "h": 926, "title": "Again", "content": passage(reference="Book 2:1")}]})
        self.assertEqual(study_factory.validate(spec), [])

    def test_the_verse_limit_counts_across_the_set_including_splits(self):
        split = {"type": "split", "left": passage(verses=verses(300, 1)), "right": passage(verses=verses(200, 1))}
        self.assertEqual(study_factory.count_verses(page_with(split)), 500)
        self.assertEqual(errors(page_with(split)), [])
        split["right"]["verses"] = verses(201, 1)
        self.assertTrue(any("501 verses" in f for f in errors(page_with(split))))

    def test_text_too_long_for_its_box_draws_the_clipping_warning(self):
        findings = study_factory.validate(page_with(passage(verses=verses(40)), h=150))
        self.assertTrue(any("will not print" in f for f in findings))


class PassageRenderTests(unittest.TestCase):
    def test_the_translation_is_the_engines_and_a_block_cannot_name_another(self):
        html = study_factory.render(page_with(passage(translation="Another version")))
        self.assertIn("NASB 2020", html)
        self.assertNotIn("Another version", html)

    def test_reference_verses_and_notice_are_escaped(self):
        html = study_factory.render(page_with(passage(reference="<i>r</i>", notice="<i>n</i>", verses=[{"number": 1, "text": "<i>t</i>"}])))
        self.assertNotIn("<i>", html)
        self.assertEqual(html.count("&lt;i&gt;"), 3)

    def test_no_notice_and_no_rows_draw_nothing_extra(self):
        html = study_factory.render(page_with(passage(notice="")))
        self.assertNotIn('<div class="passage-notice">', html)
        self.assertNotIn('<div class="grid-lines"', html)


@unittest.skipUnless(browser(), "No Chrome or Chromium here; what a page draws is not checked")
class PassagePrintTests(unittest.TestCase):
    def test_a_block_as_short_as_the_estimate_allows_still_holds_its_text(self):
        prose = "when the evening came the travellers rested beside the water and talked of the road behind them"
        pages = []
        for n, width in ((1, 760), (3, 760), (8, 760), (20, 760), (1, 373), (3, 373), (8, 373), (20, 373), (8, 244)):
            content = passage(reference=f"Book {n}:{width}", verses=[{"number": k, "text": prose} for k in range(1, n + 1)], notice=NOTICE * 3)
            need = study_factory.estimate_content_height(content, width)
            height = int(need + study_factory.HEAD_H + study_factory.BODY_TOP_PAD + 2 * study_factory.BORDER_W) + 1
            pages.append({"concept": f"{n} {width}", "title": "x", "blocks": [{"x": 28, "y": 104, "w": width, "h": height, "title": f"{n} verses at {width}", "content": content}]})
        spec = {"pages": pages}
        self.assertFalse([f for f in study_factory.validate(spec) if "will not print" in f])
        results = measure(spec)
        self.assertEqual(len(results), len(pages))
        for block in results:
            with self.subTest(block=block["title"]):
                self.assertEqual(block["overflow"], 0)


class EstimateAgreementTests(unittest.TestCase):
    def test_the_basic_example_output_is_what_the_engine_draws_now(self):
        spec = json.loads((ROOT / "shared/examples/basic/spec.json").read_text(encoding="utf-8"))
        kept = (ROOT / "shared/examples/basic/output.html").read_text(encoding="utf-8")
        self.assertEqual(kept.replace("\r\n", "\n"), study_factory.render(spec).replace("\r\n", "\n"))

    def test_the_starter_and_the_engine_use_the_same_passage_measures(self):
        script = (ROOT / "studio" / "study-starter.js").read_text(encoding="utf-8")
        for name in ("PASSAGE_REF_H", "PASSAGE_CHAR_W", "PASSAGE_LINE_H", "NOTICE_CHAR_W", "NOTICE_LINE_H"):
            with self.subTest(name=name):
                self.assertIn(f"{name} = {getattr(study_factory, name)}", script)


@unittest.skipUnless(shutil.which("node"), "Node is not installed; the generated specification is not checked here")
class StarterPassageTests(unittest.TestCase):
    def build(self, form):
        script = "const m=require(process.argv[1]);process.stdout.write(JSON.stringify(m.buildStudySpec(JSON.parse(process.argv[2]))))"
        done = subprocess.run(["node", "-e", script, str(ROOT / "studio" / "study-starter.js"), json.dumps(form)],
                              capture_output=True, text=True, encoding="utf-8", check=True)
        return json.loads(done.stdout)

    def text(self, n, words=12):
        return "\n".join(f"{k} " + " ".join(["placeholder"] * words) for k in range(1, n + 1))

    def test_pasted_text_becomes_a_passage_and_the_page_still_validates(self):
        for n in (1, 5, 8, 12, 20):
            with self.subTest(verses=n):
                spec = self.build({"title": "T", "notice": NOTICE, "sessions": [{"reference": "Book 1", "words": "a, b, c", "passage": self.text(n)}]})
                self.assertEqual(study_factory.validate(spec), [])
                blocks = spec["pages"][0]["blocks"]
                self.assertEqual(blocks[0]["content"]["type"], "passage")
                self.assertEqual(len(blocks[0]["content"]["verses"]), n)
                self.assertEqual(max(b["y"] + b["h"] for b in blocks), study_factory.SAFE_BOTTOM)

    def test_a_continuation_line_joins_its_verse_and_an_unnumbered_start_is_caught(self):
        spec = self.build({"title": "T", "notice": NOTICE, "sessions": [{"reference": "Book 1", "passage": "1 First part\nsecond part\n2 Next"}]})
        self.assertEqual(spec["pages"][0]["blocks"][0]["content"]["verses"], [{"number": 1, "text": "First part second part"}, {"number": 2, "text": "Next"}])
        spec = self.build({"title": "T", "notice": NOTICE, "sessions": [{"reference": "Book 1", "passage": "No number here"}]})
        self.assertTrue(errors(spec))

    def test_no_text_or_no_reference_stays_a_pointer_to_the_passage(self):
        spec = self.build({"title": "T", "sessions": [{"reference": "Book 1"}, {"reference": "", "passage": self.text(2)}]})
        self.assertEqual([p["blocks"][0]["content"]["type"] for p in spec["pages"]], ["callout", "callout"])
        self.assertEqual(study_factory.validate(spec), [])

    def test_an_edited_read_instruction_prints_above_the_passage(self):
        spec = self.build({"title": "T", "notice": NOTICE, "sessions": [{"reference": "Book 1", "passage": self.text(3), "read": "Read this aloud together."}]})
        self.assertEqual(spec["pages"][0]["blocks"][0]["content"]["prompt"], "Read this aloud together.")
        self.assertEqual(study_factory.validate(spec), [])


if __name__ == "__main__":
    unittest.main()
