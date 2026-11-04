"""The study starter page: served beside the Studio, and the specification it writes validates.

buildStudySpec in studio/study-starter.js is pure, so when Node is on the machine the test runs
it on a sample study and hands the result to study_factory.validate. CI's runner has Node; a
machine without it skips that check and still holds the page's structure.
"""
import json
import shutil
import subprocess
import sys
import threading
import unittest
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import study_factory  # noqa: E402
from study_studio import Handler  # noqa: E402

SAMPLE = {
    "title": "Timothy: Young and Trusted",
    "brand": "Simplify to Glorify",
    "audience": "A led class of adults at church",
    "outcome": "See that youth can still be trusted",
    "theme": "#b2c6b1",
    "sessions": [
        {"reference": "Acts 16:1-5", "title": "Chosen", "words": "circumcised, strengthened, Lystra",
         "questions": "Why did Paul want Timothy with him?\nWhat did the churches gain?"},
        {"reference": "1 Timothy 4:12-16", "title": "An example"},
        {"reference": "", "title": "", "words": "", "questions": "One question only"},
    ],
}


def build_with_node(form):
    script = "const m=require(process.argv[1]);process.stdout.write(JSON.stringify(m.buildStudySpec(JSON.parse(process.argv[2]))))"
    result = subprocess.run(["node", "-e", script, str(ROOT / "studio" / "study-starter.js"), json.dumps(form)],
                            capture_output=True, text=True, encoding="utf-8", check=True)
    return json.loads(result.stdout)


class StudyStarterPageTests(unittest.TestCase):
    def test_page_and_script_exist_and_link_each_other(self):
        html = (ROOT / "studio" / "study-starter.html").read_text(encoding="utf-8")
        script = (ROOT / "studio" / "study-starter.js").read_text(encoding="utf-8")
        index = (ROOT / "studio" / "index.html").read_text(encoding="utf-8")
        self.assertIn('href="styles.css?', html)
        self.assertIn('src="study-starter.js?', html)
        self.assertIn('href="index.html"', html)
        self.assertIn('href="study-starter.html"', index)
        self.assertIn("function buildStudySpec", script)
        for text in (html, script):
            self.assertNotIn("�", text)
            self.assertNotIn("Ã", text)

    def test_server_serves_the_page(self):
        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{server.server_port}/study-starter.html") as response:
                self.assertEqual(response.status, 200)
                self.assertIn("text/html", response.headers["Content-Type"])
                self.assertIn(b"Study starter", response.read())
        finally:
            server.shutdown()
            server.server_close()


@unittest.skipUnless(shutil.which("node"), "Node is not installed; the generated specification is not checked here")
class StudyStarterSpecTests(unittest.TestCase):
    def setUp(self):
        self.spec = build_with_node(SAMPLE)

    def test_one_page_per_session_plus_a_discussion_page_when_questions_are_given(self):
        labels = [p["label"] for p in self.spec["pages"]]
        self.assertEqual(labels, ["Session 1", "Session 1 · Discuss", "Session 2", "Session 3", "Session 3 · Discuss"])
        self.assertEqual(self.spec["set_title"], "Timothy: Young and Trusted")
        self.assertEqual(self.spec["footer_label"], "Simplify to Glorify | Timothy: Young and Trusted")

    def test_the_specification_validates_with_no_findings(self):
        self.assertEqual(study_factory.validate(self.spec), [])

    def test_blank_fields_take_wording_that_names_the_passage(self):
        page = self.spec["pages"][2]
        self.assertEqual(page["title"], "SESSION 2: AN EXAMPLE")
        self.assertIn("1 Timothy 4:12-16", page["blocks"][1]["content"]["prompt"])
        self.assertEqual(page["blocks"][2]["title"], "Session 2 · Questions")

    def test_a_session_with_nothing_filled_in_still_lays_out(self):
        page = self.spec["pages"][3]
        self.assertEqual(page["title"], "SESSION 3: SESSION 3")
        self.assertEqual(page["blocks"][0]["title"], "Session 3 · Read the passage")

    def test_every_page_reaches_the_fill_target_and_stays_inside_the_sheet(self):
        for page in self.spec["pages"]:
            bottoms = [b["y"] + b["h"] for b in page["blocks"]]
            self.assertEqual(max(bottoms), study_factory.SAFE_BOTTOM)
            for b in page["blocks"]:
                self.assertGreaterEqual(b["x"], study_factory.CONTENT_LEFT)
                self.assertLessEqual(b["x"] + b["w"], study_factory.CONTENT_RIGHT)

    def test_too_many_words_and_questions_are_capped_not_overflowed(self):
        form = json.loads(json.dumps(SAMPLE))
        form["sessions"] = [{"reference": "Psalm 23", "words": ", ".join(f"word{i}" for i in range(14)),
                             "questions": "\n".join(f"Question {i}?" for i in range(6))}]
        spec = build_with_node(form)
        self.assertEqual(len(spec["pages"][0]["blocks"][2]["content"]["items"]), 10)
        self.assertEqual(len(spec["pages"][1]["blocks"]), 4)
        self.assertEqual(study_factory.validate(spec), [])


if __name__ == "__main__":
    unittest.main()
