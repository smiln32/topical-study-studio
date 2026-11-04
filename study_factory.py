#!/usr/bin/env python3
"""Generate full-page, print-ready US Letter study pages as HTML from JSON.

The output uses ordinary HTML text, divs, borders, checkboxes, lines, and tables,
so the pages print crisply from a browser and stay editable as HTML.

Usage:
    python study_factory.py study_spec.json output.html
    python study_factory.py study_spec.json output.html --validate-only
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from html import escape
from pathlib import Path
from typing import Any

PAGE_W = 816
PAGE_H = 1056
HEADER_TOP = 24
HEADER_H = 66
FOOTER_BOTTOM = 10
SAFE_BOTTOM = 1030
FILL_TARGET = 980
VERSION = "1.1.0"
CONTENT_TOP, CONTENT_BOTTOM, CONTENT_W, GAP = 104, 1030, 760, 14
CONTENT_LEFT = 28
CONTENT_RIGHT = CONTENT_LEFT + CONTENT_W
MIN_BLOCK_W = 180
MIN_BLOCK_H = 92

CSS = r"""
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:#ececec;font-family:"Aptos","Helvetica Neue",Arial,sans-serif;color:#343a38}
@page{size:Letter;margin:0}
.page{position:relative;width:816px;height:1056px;margin:0 auto;background:#fff;page-break-after:always;overflow:hidden}
.page:last-child{page-break-after:auto}
.header{position:absolute;left:28px;top:24px;width:760px;height:66px;border-radius:10px;background:var(--theme);display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:0 16px}
.title{max-width:100%;font-family:Georgia,"Times New Roman",serif;font-size:23px;font-weight:700;line-height:1.05;letter-spacing:-.25px;margin:0 0 5px;text-wrap:balance;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;overflow-wrap:anywhere}
.subtitle{max-width:100%;font-size:10px;line-height:1.1;color:#4d4d4d;margin:0;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;overflow-wrap:anywhere}
.footer{position:absolute;left:28px;bottom:10px;width:760px;height:16px;display:flex;justify-content:space-between;align-items:center;font-size:8px;color:#8c8c8c}
.box{position:absolute;border:1.2px solid #5c5c5c;border-radius:10px;background:#fff;overflow:hidden}
.head{height:32px;display:flex;align-items:center;padding:0 12px;font-size:10.5px;font-weight:700;border-bottom:1.2px solid #5c5c5c;letter-spacing:.15px}
.sage{background:#dfe9df}.lav{background:#e8dfea}.blue{background:#dce8ee}.warm{background:#f0e6e2}.rose{background:#eee0dd}.ivory{background:#fbf9f6}
.body{height:calc(100% - 32px);padding:11px 13px;background:#fff;display:flex;flex-direction:column}
.body>*{flex:none}
.prompt{font-size:9px;font-weight:700;margin:0 0 4px}
.line{height:22px;border-bottom:1px solid #b9b9b9}
.line.tight{height:18px}.line.tall{height:27px}
.grid-lines{display:grid;height:100%;grid-template-rows:repeat(var(--rows),1fr);gap:0}
.body>.grid-lines,.body>.two-col>div>.grid-lines{flex:1 1 0;height:auto;min-height:0;grid-template-rows:repeat(var(--rows),minmax(0,1fr))}
.body>.grid-lines>.line,.body>.two-col>div>.grid-lines>.line{height:auto;min-height:0}
.check-row{display:grid;grid-template-columns:14px 1fr;gap:8px;align-items:center;height:24px;font-size:9.5px}
.check{width:10px;height:10px;border:1px solid #5c5c5c}
.radio{width:10px;height:10px;border:1px solid #5c5c5c;border-radius:50%}
.pill-row{display:flex;gap:12px;flex-wrap:wrap;align-items:center;font-size:9px;margin-bottom:4px}
.pill{display:flex;align-items:center;gap:5px}
.two-col{display:grid;grid-template-columns:1fr 1fr;gap:12px;height:100%}
.body>.two-col{flex:1 1 0;height:auto;min-height:0;grid-template-rows:minmax(0,1fr)}
.body>.two-col>div{display:flex;flex-direction:column;min-width:0;min-height:0}
.body>.two-col>div>*{flex:none}
.body>.custom{flex:1 1 0;min-height:0}
.label{font-size:9.5px;font-weight:700;margin-bottom:4px}
.small{font-size:8.5px;color:#555}.callout{font-size:10px;line-height:1.35}
.passage-ref{display:flex;justify-content:space-between;gap:12px;font-size:10.5px;font-weight:700;margin-bottom:4px}
.passage-translation{font-size:8.5px;font-weight:400;color:#555;white-space:nowrap}
.passage-text{font-size:11px;line-height:1.4}
.passage-text sup{font-size:8.5px;font-weight:700;line-height:0;margin-right:2px}
.passage-notice{font-size:8.5px;line-height:1.25;color:#555;margin-top:4px}
.table{width:100%;border-collapse:collapse;table-layout:fixed;font-size:8px}
.table th,.table td{border:1px solid #7f7f7f;padding:4px;vertical-align:top}
.table th{background:#f5f5f5;font-weight:800;text-transform:uppercase;text-align:center}
.table td{height:31px}.center{text-align:center}
"""


def e(value: Any) -> str:
    return escape(str(value), quote=True)


def line_html(rows: int, line_class: str = "line") -> str:
    return "".join(f'<div class="{e(line_class)}"></div>' for _ in range(rows))


def checklist_html(items: list[str], blank_rows: int = 0) -> str:
    out = []
    for item in items:
        out.append(f'<div class="check-row"><div class="check"></div><div>{e(item)}</div></div>')
    for _ in range(blank_rows):
        out.append('<div class="check-row"><div class="check"></div><div class="line tight"></div></div>')
    return "".join(out)


def choices_html(options: list[str], control: str = "radio", lines_after: int = 0) -> str:
    control_class = "radio" if control == "radio" else "check"
    pills = "".join(
        f'<div class="pill"><div class="{control_class}"></div><span>{e(opt)}</span></div>'
        for opt in options
    )
    return f'<div class="pill-row">{pills}</div>' + line_html(lines_after)


def render_content(content: dict[str, Any]) -> str:
    kind = content.get("type", "lines")
    prompt = content.get("prompt")
    prefix = f'<div class="prompt">{e(prompt)}</div>' if prompt else ""

    if kind == "lines":
        rows = int(content.get("rows", 6))
        return prefix + f'<div class="grid-lines" style="--rows:{rows}">{line_html(rows)}</div>'

    if kind == "checklist":
        return prefix + checklist_html(
            [str(x) for x in content.get("items", [])],
            int(content.get("blank_rows", 0)),
        )

    if kind == "choices":
        return prefix + choices_html(
            [str(x) for x in content.get("options", [])],
            str(content.get("control", "radio")),
            int(content.get("lines_after", 0)),
        )

    if kind == "callout":
        text = content.get("text", "")
        rows = int(content.get("rows", 0))
        callout = f'<div class="callout">{e(text)}</div>'
        return prefix + callout + (f'<div class="grid-lines" style="--rows:{rows}">{line_html(rows)}</div>' if rows else "")

    if kind == "passage":
        verses = "".join(f'<sup>{e(v["number"])}</sup>{e(v["text"])} ' for v in content.get("verses", []))
        notice = content.get("notice")
        rows = int(content.get("rows", 0))
        return (
            prefix
            + f'<div class="passage-ref"><span>{e(content.get("reference", ""))}</span><span class="passage-translation">{e(SCRIPTURE_TRANSLATION)}</span></div>'
            + f'<div class="passage-text">{verses}</div>'
            + (f'<div class="passage-notice">{e(notice)}</div>' if notice else "")
            + (f'<div class="grid-lines" style="--rows:{rows}">{line_html(rows)}</div>' if rows else "")
        )

    if kind == "table":
        columns = content.get("columns", [])
        rows = int(content.get("rows", 10))
        th = []
        for col in columns:
            width = col.get("width")
            style = f' style="width:{e(width)}"' if width else ""
            th.append(f'<th{style}>{e(col.get("label", ""))}</th>')
        td_row = "<tr>" + "".join("<td></td>" for _ in columns) + "</tr>"
        return prefix + f'<table class="table"><tr>{"".join(th)}</tr>{td_row * rows}</table>'

    if kind == "split":
        left = render_content(content.get("left", {"type": "lines", "rows": 5}))
        right = render_content(content.get("right", {"type": "lines", "rows": 5}))
        return prefix + f'<div class="two-col"><div>{left}</div><div>{right}</div></div>'

    if kind == "custom_html":
        # Deliberately opt-in. The JSON author is responsible for valid HTML.
        return prefix + '<div class="custom">' + str(content.get("html", "")) + "</div>"

    raise ValueError(f"Unsupported content type: {kind}")


def render_box(block: dict[str, Any]) -> str:
    x = int(block["x"]); y = int(block["y"])
    w = int(block["w"]); h = int(block["h"])
    title = e(block.get("title", ""))
    color = e(block.get("color", "sage"))
    body = render_content(block.get("content", {"type": "lines", "rows": 6}))
    return (
        f'<div class="box" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">'
        f'<div class="head {color}">{title}</div><div class="body">{body}</div></div>'
    )


def normalize_phrase(value: Any) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(value).lower()).strip()


def validate_uniqueness_and_collisions(spec: dict[str, Any]) -> list[str]:
    findings, concepts, section_titles, prompts = [], {}, {}, {}
    for page_no, page in enumerate(spec.get("pages", []), 1):
        concept = normalize_phrase(page.get("concept", page.get("title", "")))
        if concept in concepts: findings.append(f"ERROR: Pages {concepts[concept]} and {page_no} repeat the same concept.")
        elif concept: concepts[concept] = page_no
        blocks = page.get("blocks", [])
        for block_no, block in enumerate(blocks, 1):
            content = block.get("content", {})
            for label, value, seen in (
                ("section title", block.get("title", ""), section_titles),
                ("prompt", content.get("prompt", "") if isinstance(content, dict) else "", prompts),
            ):
                phrase = normalize_phrase(value)
                if phrase and phrase in seen:
                    first_page, first_block = seen[phrase]
                    findings.append(
                        f"Page {page_no}, block {block_no}: repeats {label} from "
                        f"page {first_page}, block {first_block}."
                    )
                elif phrase:
                    seen[phrase] = (page_no, block_no)
        boxes = []
        for n, block in enumerate(blocks, 1):
            try: boxes.append((n, *(int(block[k]) for k in ("x", "y", "w", "h"))))
            except (KeyError, TypeError, ValueError, OverflowError): continue  # already reported by validate()
        for i, (a, ax, ay, aw, ah) in enumerate(boxes):
            for b, bx, by, bw, bh in boxes[i + 1:]:
                dx = max(bx - (ax + aw), ax - (bx + bw))  # horizontal distance between edges; negative when they share columns
                dy = max(by - (ay + ah), ay - (by + bh))  # vertical distance between edges; negative when they share rows
                if dx < 0 and dy < 0:
                    findings.append(f"ERROR: Page {page_no}, blocks {a} and {b} overlap.")
                elif (dx < 0 or dy < 0) and max(dx, dy) < GAP:
                    findings.append(f"Page {page_no}, blocks {a} and {b} are {max(dx, dy)}px apart; the standard gap is {GAP}px.")
    return findings
CONTENT_TYPES = ("lines", "checklist", "choices", "callout", "passage", "table", "split", "custom_html")
SCRIPTURE_TRANSLATION = "NASB 2020"  # the one translation quoted; CLAUDE.md, so a block cannot name another
MAX_VERSES = 500  # the owner's limit for one work; DECISIONS.md
# The count field each content type reads; split and custom_html read none.
COUNT_FIELDS = {"lines": "rows", "checklist": "blank_rows", "choices": "lines_after", "callout": "rows", "passage": "rows", "table": "rows"}
MAX_COUNT = 200  # more rows than any page can hold
CSS_COLOR_NAMES = frozenset("""aliceblue antiquewhite aqua aquamarine azure beige bisque black blanchedalmond blue blueviolet brown
burlywood cadetblue chartreuse chocolate coral cornflowerblue cornsilk crimson cyan darkblue darkcyan darkgoldenrod darkgray
darkgreen darkgrey darkkhaki darkmagenta darkolivegreen darkorange darkorchid darkred darksalmon darkseagreen darkslateblue
darkslategray darkslategrey darkturquoise darkviolet deeppink deepskyblue dimgray dimgrey dodgerblue firebrick floralwhite
forestgreen fuchsia gainsboro ghostwhite gold goldenrod gray green greenyellow grey honeydew hotpink indianred indigo ivory
khaki lavender lavenderblush lawngreen lemonchiffon lightblue lightcoral lightcyan lightgoldenrodyellow lightgray lightgreen
lightgrey lightpink lightsalmon lightseagreen lightskyblue lightslategray lightslategrey lightsteelblue lightyellow lime
limegreen linen magenta maroon mediumaquamarine mediumblue mediumorchid mediumpurple mediumseagreen mediumslateblue
mediumspringgreen mediumturquoise mediumvioletred midnightblue mintcream mistyrose moccasin navajowhite navy oldlace olive
olivedrab orange orangered orchid palegoldenrod palegreen paleturquoise palevioletred papayawhip peachpuff peru pink plum
powderblue purple rebeccapurple red rosybrown royalblue saddlebrown salmon sandybrown seagreen seashell sienna silver skyblue
slateblue slategray slategrey snow springgreen steelblue tan teal thistle tomato turquoise violet wheat white whitesmoke
yellow yellowgreen transparent""".split())
HEX_COLOR_RE = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")
# rgb()/hsl() with three numbers, each with an optional unit, and an optional fourth for alpha
_N = r"[0-9]*\.?[0-9]+(deg|rad|grad|turn|%)?"
FUNC_COLOR_RE = re.compile(rf"^(rgb|rgba|hsl|hsla)\(\s*{_N}\s*[,\s]\s*{_N}\s*[,\s]\s*{_N}\s*([,/]\s*{_N}\s*)?\)$")


def is_color(value: Any) -> bool:
    """A colour the browser will accept: a hex code, a CSS colour name, or an rgb()/hsl() value."""
    if not isinstance(value, str): return False
    return bool(HEX_COLOR_RE.match(value) or value.lower() in CSS_COLOR_NAMES or FUNC_COLOR_RE.match(value))
LENGTH_RE = re.compile(r"^\d+(\.\d+)?(%|px|em|rem)$")


# A block's head is 32px and its body starts 11px below that, inside a 1.2px border top and bottom.
# The body's 11px bottom padding sits inside the clipping box, so content may run into it and
# still print; past it, the box cuts it off. Row heights were measured in Chrome.
HEAD_H, BODY_TOP_PAD, BORDER_W, LINE_H, CHECK_H, TABLE_ROW_H, TABLE_HEAD_H, PROMPT_H, PILL_H = 32, 11, 1.2, 22, 24, 31, 21, 16, 14
TITLE_CHARS = 90
PASSAGE_REF_H, PASSAGE_CHAR_W, PASSAGE_LINE_H, NOTICE_CHAR_W, NOTICE_LINE_H = 20, 5.6, 15.4, 4.4, 10.7


def is_count(value: Any) -> bool:
    """A whole number of rows: a non-negative int, or a string of digits. Not a bool, float or negative."""
    if isinstance(value, bool): return False
    if isinstance(value, int): return 0 <= value <= MAX_COUNT
    return isinstance(value, str) and value.isdigit() and int(value) <= MAX_COUNT


def _count(content: dict[str, Any], field: str, default: int) -> int:
    value = content.get(field, default)
    return int(value) if is_count(value) else default


def estimate_content_height(content: Any, width: int) -> float:
    """Roughly how tall the content renders, in px, so a box that clips can be named."""
    if not isinstance(content, dict): return 0
    kind = content.get("type", "lines")
    total = PROMPT_H if content.get("prompt") else 0
    if kind == "lines": total += _count(content, "rows", 6) * LINE_H
    elif kind == "checklist":
        items = content.get("items", [])
        total += ((len(items) if isinstance(items, list) else 0) + _count(content, "blank_rows", 0)) * CHECK_H
    elif kind == "choices": total += PILL_H + _count(content, "lines_after", 0) * LINE_H
    elif kind == "callout":
        chars_per_line = max(20, (width - 2 * 13) // 5)
        total += -(-len(str(content.get("text", ""))) // chars_per_line) * 14 + _count(content, "rows", 0) * LINE_H
    elif kind == "passage":
        verses = content.get("verses", [])
        chars = sum(len(str(v.get("text", ""))) + len(str(v.get("number", ""))) + 1 for v in verses if isinstance(v, dict)) if isinstance(verses, list) else 0
        notice = str(content.get("notice") or "")
        inner = width - 2 * 13
        total += PASSAGE_REF_H + -(-chars // int(inner / PASSAGE_CHAR_W)) * PASSAGE_LINE_H + _count(content, "rows", 0) * LINE_H
        if notice: total += 4 + -(-len(notice) // int(inner / NOTICE_CHAR_W)) * NOTICE_LINE_H
    elif kind == "table": total += TABLE_HEAD_H + _count(content, "rows", 10) * TABLE_ROW_H
    elif kind == "split":
        default = {"type": "lines", "rows": 5}  # what render_content draws for a missing side
        total += max(estimate_content_height(content.get(side, default), (width - 12) // 2) for side in ("left", "right"))
    return total


def uses_custom_html(spec: Any) -> bool:
    """True when any block, or either side of a split, is custom_html."""
    def walk(content: Any) -> bool:
        if not isinstance(content, dict): return False
        if content.get("type") == "custom_html": return True
        return any(walk(content.get(side)) for side in ("left", "right"))
    if not isinstance(spec, dict) or not isinstance(spec.get("pages"), list): return False
    return any(
        walk(block.get("content"))
        for page in spec["pages"] if isinstance(page, dict) and isinstance(page.get("blocks"), list)
        for block in page["blocks"] if isinstance(block, dict)
    )


def passages(spec: Any) -> list[dict[str, Any]]:
    """Every passage content object in a set, including either side of a split."""
    found: list[dict[str, Any]] = []
    def walk(content: Any) -> None:
        if not isinstance(content, dict): return
        if content.get("type") == "passage": found.append(content)
        for side in ("left", "right"): walk(content.get(side))
    if isinstance(spec, dict) and isinstance(spec.get("pages"), list):
        for page in spec["pages"]:
            if isinstance(page, dict) and isinstance(page.get("blocks"), list):
                for block in page["blocks"]:
                    if isinstance(block, dict): walk(block.get("content"))
    return found


def count_verses(spec: Any) -> int:
    """Verses quoted across a set. A verse quoted twice counts twice, which errs on the safe side."""
    return sum(len(p["verses"]) for p in passages(spec) if isinstance(p.get("verses"), list))


def validate_shape(spec: Any) -> list[str]:
    """Report a specification whose shape the other checks cannot read."""
    if not isinstance(spec, dict):
        return ['ERROR: The specification must be a JSON object with a "pages" list.']
    pages = spec.get("pages", [])
    if not isinstance(pages, list):
        return ['ERROR: "pages" must be a list of page objects.']
    findings = []
    for idx, page in enumerate(pages, start=1):
        if not isinstance(page, dict):
            findings.append(f"ERROR: Page {idx} must be an object."); continue
        blocks = page.get("blocks", [])
        if not isinstance(blocks, list):
            findings.append(f'ERROR: Page {idx}: "blocks" must be a list of block objects.'); continue
        for n, block in enumerate(blocks, start=1):
            if not isinstance(block, dict):
                findings.append(f"ERROR: Page {idx}, block {n} must be an object.")
    return findings


def validate_content(content: Any, where: str) -> list[str]:
    """Report content that render_content could not draw."""
    if not isinstance(content, dict):
        return [f'ERROR: {where}: "content" must be an object.']
    findings = []
    kind = content.get("type", "lines")
    if kind not in CONTENT_TYPES:
        findings.append(f"ERROR: {where}: unknown content type {kind!r}. Use one of: {', '.join(CONTENT_TYPES)}.")
    field = COUNT_FIELDS.get(kind)
    if field and field in content and not is_count(content[field]):
        findings.append(f'ERROR: {where}: "{field}" must be a whole number from 0 to {MAX_COUNT}, not {content[field]!r}.')
    for field in ("items", "options"):
        if field in content and not isinstance(content[field], list):
            findings.append(f'ERROR: {where}: "{field}" must be a list.')
    if kind == "passage":
        reference = content.get("reference")
        if not (isinstance(reference, str) and reference.strip()):
            findings.append(f'ERROR: {where}: a passage needs a "reference", such as "Psalm 23:1-3".')
        verses = content.get("verses")
        if not (isinstance(verses, list) and verses):
            findings.append(f'ERROR: {where}: a passage needs "verses", a list of objects each with a "number" and "text".')
        else:
            for k, verse in enumerate(verses, 1):
                number = verse.get("number") if isinstance(verse, dict) else None
                text = verse.get("text") if isinstance(verse, dict) else None
                if not ((isinstance(number, int) and not isinstance(number, bool) and number > 0) or (isinstance(number, str) and number.isdigit() and int(number) > 0)):
                    findings.append(f'ERROR: {where}: verse {k} needs a "number", a whole number above 0.')
                if not (isinstance(text, str) and text.strip()):
                    findings.append(f'ERROR: {where}: verse {k} needs its "text".')
        if "notice" in content and not isinstance(content["notice"], str):
            findings.append(f'ERROR: {where}: "notice" must be text.')
    if kind == "table":
        columns = content.get("columns", [])
        if not isinstance(columns, list) or not all(isinstance(c, dict) for c in columns):
            findings.append(f'ERROR: {where}: table "columns" must be a list of objects, each with a "label".')
        elif not all(isinstance(c.get("label", ""), str) for c in columns):
            findings.append(f'ERROR: {where}: every table column "label" must be text.')
        else:
            for c in columns:
                width = c.get("width")
                if width is not None and not (isinstance(width, str) and LENGTH_RE.match(width)):
                    findings.append(f'ERROR: {where}: column width {width!r} is not a length. Use a percentage such as "15%".')
    if kind == "split":
        for side in ("left", "right"):
            if side in content:
                findings.extend(validate_content(content[side], f"{where}, {side} side"))
    return findings


def validate(spec: dict[str, Any]) -> list[str]:
    shape_findings = validate_shape(spec)
    if shape_findings:
        return shape_findings
    warnings: list[str] = []
    pages = spec.get("pages", [])
    if not pages:
        warnings.append("ERROR: No pages were defined.")
        return warnings

    for idx, page in enumerate(pages, start=1):
        title = str(page.get("title", ""))
        if len(title) > TITLE_CHARS:
            warnings.append(f"Page {idx}: the title is {len(title)} characters; the header shows about two lines ({TITLE_CHARS} characters) and hides the rest.")
        theme = page.get("theme")
        if theme is not None and not is_color(theme):
            warnings.append(f"ERROR: Page {idx}: theme {theme!r} is not a colour. Use a hex code such as #b2c6b1 or a colour name.")
        blocks = page.get("blocks", [])
        if not blocks:
            warnings.append(f"Page {idx}: no blocks defined.")
            continue
        bottoms = []
        for n, block in enumerate(blocks, start=1):
            warnings.extend(validate_content(block.get("content", {}), f"Page {idx}, block {n}"))
            try:
                x, y, w, h = (int(block[k]) for k in ("x", "y", "w", "h"))
            except (KeyError, TypeError, ValueError, OverflowError):
                warnings.append(f"ERROR: Page {idx}, block {n}: invalid x/y/w/h.")
                continue
            if w < MIN_BLOCK_W or h < MIN_BLOCK_H:
                warnings.append(f"ERROR: Page {idx}, block {n}: block must be at least {MIN_BLOCK_W} x {MIN_BLOCK_H}px.")
            if x < CONTENT_LEFT or x + w > CONTENT_RIGHT:
                warnings.append(f"ERROR: Page {idx}, block {n}: outside the horizontal safe area ({CONTENT_LEFT}-{CONTENT_RIGHT}px).")
            if y < CONTENT_TOP:
                warnings.append(f"ERROR: Page {idx}, block {n}: begins above the content area ({CONTENT_TOP}px).")
            if y + h > SAFE_BOTTOM:
                warnings.append(f"ERROR: Page {idx}, block {n}: extends below the safe content bottom ({SAFE_BOTTOM}px).")
            bottoms.append(y + h)
            body_h, need = h - HEAD_H - BODY_TOP_PAD - 2 * BORDER_W, estimate_content_height(block.get("content", {}), w)
            if need > body_h:
                warnings.append(
                    f"Page {idx}, block {n} ({block.get('title', 'untitled')}): about {round(need)}px of content in a {round(body_h)}px body; "
                    f"what runs past the bottom will not print. Remove rows or make the block taller."
                )
        if bottoms and max(bottoms) < FILL_TARGET:
            warnings.append(
                f"Page {idx}: content stops at {max(bottoms)}px; extend it to at least {FILL_TARGET}px so the page feels full."
            )
    warnings.extend(validate_uniqueness_and_collisions(spec))
    quoted = count_verses(spec)
    if quoted > MAX_VERSES:
        warnings.append(f"ERROR: This set quotes {quoted} verses; one work may quote at most {MAX_VERSES}.")
    if passages(spec) and not any(isinstance(p.get("notice"), str) and p["notice"].strip() for p in passages(spec)):
        warnings.append(f'This set quotes Scripture and prints no copyright notice. Give a passage a "notice", copied from the publisher, or print it elsewhere in the work.')
    return warnings


def render(spec: dict[str, Any]) -> str:
    set_title = e(spec.get("set_title", "Study"))
    footer_label = e(spec.get("footer_label", "Study"))
    pages = []
    for idx, page in enumerate(spec.get("pages", []), start=1):
        theme = e(page.get("theme", "#b2c6b1"))
        title = e(page.get("title", f"PAGE {idx}"))
        subtitle = e(page.get("subtitle", ""))
        blocks = "".join(render_box(b) for b in page.get("blocks", []))
        label = e(page.get("label", page.get("title", f"Page {idx}")))
        pages.append(
            f'<section class="page" data-document-role="page" data-label="{label}" style="--theme:{theme}">'
            f'<div class="header"><div class="title">{title}</div><div class="subtitle">{subtitle}</div></div>'
            f'{blocks}'
            f'<div class="footer"><span>{footer_label}</span><span>{idx} of {len(spec.get("pages", []))}</span></div>'
            f'</section>'
        )
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{set_title}</title><style>{CSS}</style></head><body>'
        + "".join(pages)
        + '</body></html>'
    )


def starter_spec(topic: str) -> dict[str, Any]:
    topic = topic.strip() or "Untitled"
    return {
        "set_title": f"{topic} Study",
        "footer_label": f"Simplify to Glorify | {topic} Study",
        "pages": [
            {
                "label": "Session 1",
                "concept": f"See what the passage says about {topic}",
                "title": f"Session 1: {topic}",
                "subtitle": "Name the passage here. Read all of it before you begin.",
                "theme": "#b2c6b1",
                "blocks": [
                    {"x": 28, "y": 104, "w": 760, "h": 150, "title": "Read the passage", "color": "sage", "content": {"type": "callout", "text": "Read the passage twice in the NASB 2020, once silently and once aloud. Then write out the verse that speaks most clearly to you.", "rows": 3}},
                    {"x": 28, "y": 268, "w": 373, "h": 300, "title": "Observe", "color": "blue", "content": {"type": "lines", "prompt": "What does the text say? Note every action and repeated word.", "rows": 10}},
                    {"x": 415, "y": 268, "w": 373, "h": 300, "title": "Words to look up", "color": "lav", "content": {"type": "checklist", "items": ["First word", "Second word"], "blank_rows": 8}},
                    {"x": 28, "y": 582, "w": 760, "h": 448, "title": "Interpret and apply", "color": "warm", "content": {"type": "split", "left": {"type": "lines", "prompt": "What did it mean to the people who first heard it?", "rows": 17}, "right": {"type": "lines", "prompt": "What does it ask of me this week?", "rows": 17}}}
                ]
            }
        ]
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate and validate printable study pages.")
    parser.add_argument("spec", nargs="?", type=Path, help="Study JSON specification")
    parser.add_argument("output", nargs="?", type=Path, help="Output HTML path")
    parser.add_argument("--validate-only", action="store_true", help="Validate without writing HTML")
    parser.add_argument("--init", dest="init_path", type=Path, metavar="PATH", help="Create a starter JSON specification")
    parser.add_argument("--topic", default="Untitled", help="Topic used with --init (default: Untitled)")
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    args = parser.parse_args()

    if args.init_path:
        if args.spec or args.output or args.validate_only:
            parser.error("--init cannot be combined with spec/output arguments or --validate-only")
        args.init_path.write_text(json.dumps(starter_spec(args.topic), indent=2) + "\n", encoding="utf-8")
        print(f"Created starter specification: {args.init_path}")
        return 0

    if not args.spec or not args.output:
        parser.error("spec and output are required unless --init or --version is used")

    try:
        spec = json.loads(args.spec.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        print(f"Could not read specification: {exc}", file=sys.stderr)
        return 2

    try:
        warnings = validate(spec)
        for warning in warnings:
            print(warning, file=sys.stderr)
        if uses_custom_html(spec):
            print("Note: this specification contains custom HTML, which is inserted unescaped. "
                  "Only generate specifications from authors you trust.", file=sys.stderr)
        if any(warning.startswith("ERROR") for warning in warnings):
            print(f"Validation failed with {len(warnings)} finding(s).", file=sys.stderr)
            return 2

        page_count = len(spec.get("pages", []))
        block_count = sum(len(page.get("blocks", [])) for page in spec.get("pages", []))
        if args.validate_only:
            if warnings:
                print(f"Validation completed with {len(warnings)} warning(s): {page_count} page(s), {block_count} block(s).")
                return 1
            print(f"Validation passed: {page_count} page(s), {block_count} block(s).")
            return 0

        args.output.write_text(render(spec), encoding="utf-8")
        print(f"Generated {page_count} page(s) with {block_count} block(s): {args.output}")
        return 0

    except Exception as exc:  # a shape the checks above did not foresee
        print(f"Could not generate: {exc}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
