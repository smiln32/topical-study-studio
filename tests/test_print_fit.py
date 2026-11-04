"""What Chrome draws: every writing line of an engine-drawn block prints, at a usable height.

The validator estimates; only a browser can see a line cut off by its box. A machine with no
Chrome or Chromium skips these checks.
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import study_factory  # noqa: E402

MEASURE = """<script>addEventListener('load',()=>{const out=[];document.querySelectorAll('.box').forEach(b=>{
const edge=b.getBoundingClientRect().bottom;const ls=[...b.querySelectorAll('.line')].map(l=>l.getBoundingClientRect());
out.push({title:b.querySelector('.head').textContent,lines:ls.length,cut:ls.filter(l=>l.bottom>edge-1).length,
smallest:ls.length?Math.min(...ls.map(l=>l.height)):null})});
const d=document.createElement('pre');d.id='RESULT';d.textContent=JSON.stringify(out);document.body.appendChild(d)})</script>"""


def browser():
    for name in ("chrome", "google-chrome", "chromium", "chromium-browser", "msedge"):
        found = shutil.which(name)
        if found:
            return found
    for path in ("C:/Program Files/Google/Chrome/Application/chrome.exe", "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
                 "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"):
        if Path(path).exists():
            return path
    return None


def measure(spec):
    with tempfile.TemporaryDirectory() as folder:
        page = Path(folder) / "page.html"
        page.write_text(study_factory.render(spec).replace("</body>", MEASURE + "</body>"), encoding="utf-8")
        dom = subprocess.run([browser(), "--headless", "--disable-gpu", "--no-sandbox", "--virtual-time-budget=2000", "--dump-dom", page.as_uri()],
                             capture_output=True, text=True, encoding="utf-8", timeout=60).stdout
    return json.loads(unescape(re.search(r'id="RESULT">(.*?)</pre>', dom, re.S).group(1)))


def one_page(*blocks):
    return {"pages": [{"concept": "x", "title": "x", "blocks": list(blocks)}]}


@unittest.skipUnless(browser(), "No Chrome or Chromium here; what a page draws is not checked")
class PrintFitTests(unittest.TestCase):
    def assert_all_lines_print(self, results):
        self.assertTrue(results)
        for block in results:
            with self.subTest(block=block["title"]):
                self.assertEqual(block["cut"], 0)
                if block["lines"]:
                    self.assertGreaterEqual(block["smallest"], 18)

    def test_a_prompted_block_prints_its_last_line(self):
        prompt = "A prompt long enough to wrap onto a second line in a half-width block, because that costs the rows more height."
        self.assert_all_lines_print(measure(one_page(
            {"x": 28, "y": 104, "w": 373, "h": 300, "title": "lines", "content": {"type": "lines", "prompt": prompt, "rows": 10}},
            {"x": 415, "y": 104, "w": 373, "h": 300, "title": "callout", "content": {"type": "callout", "text": "Guidance. " * 12, "rows": 9}},
            {"x": 28, "y": 418, "w": 760, "h": 234, "title": "split", "content": {
                "type": "split", "left": {"type": "lines", "prompt": prompt, "rows": 7}, "right": {"type": "lines", "prompt": "Short", "rows": 7}}},
        )))

    def test_the_study_example_prints_every_line(self):
        self.assert_all_lines_print(measure(json.loads((ROOT / "shared/examples/study/spec.json").read_text(encoding="utf-8"))))

    def test_custom_html_keeps_the_sizing_its_author_wrote_against(self):
        rows = '<div class="grid-lines" style="--rows:4">' + '<div class="line"></div>' * 4 + "</div>"
        two = f'<div class="two-col"><div>{rows}</div><div>{rows}</div></div>'
        results = measure(one_page(
            {"x": 28, "y": 104, "w": 760, "h": 200, "title": "custom", "content": {"type": "custom_html", "html": rows}},
            {"x": 28, "y": 318, "w": 760, "h": 200, "title": "custom split", "content": {"type": "custom_html", "html": two}},
        ))
        for block in results:
            with self.subTest(block=block["title"]):
                self.assertEqual(block["smallest"], 22)


if __name__ == "__main__":
    unittest.main()
