# Study Specification Reference

Topical Study Studio reads a UTF-8 JSON document and renders each entry in `pages` as an editable 816 × 1056 px US Letter page.

## Create a starter file

```bash
python study_factory.py --init my-study.json --topic "Psalm 23"
```

Then validate and generate it:

```bash
python study_factory.py my-study.json output.html --validate-only
python study_factory.py my-study.json output.html
```

## Top-level fields

| Field | Required | Type | Purpose |
|---|---:|---|---|
| `set_title` | No | string | HTML document title. Defaults to `Study`. |
| `footer_label` | No | string | Left side of every page footer. Defaults to `Study`. |
| `pages` | Yes | array | Ordered list of study pages. At least one page is required. |

## Page fields

| Field | Required | Type | Purpose |
|---|---:|---|---|
| `concept` | Recommended | string | The page's single useful job. Must be unique across the set. |
| `label` | No | string | Page label, written to the page section as a `data-label` attribute. Defaults to the page title. |
| `title` | No | string | Main page heading. |
| `subtitle` | No | string | Short supportive explanation beneath the title. |
| `theme` | No | CSS color | Header color: a hex code such as `#b2c6b1`, one of the CSS color names, or an `rgb()`/`hsl()` value with three numbers and an optional alpha. Anything else is an error. Defaults to `#b2c6b1`. |
| `blocks` | Yes | array | Positioned content containers. |

## Block fields

Every block uses absolute pixel geometry on the 816 × 1056 canvas.

| Field | Required | Type | Purpose |
|---|---:|---|---|
| `x` | Yes | integer | Distance from the left edge. Standard outer edge: `28`. |
| `y` | Yes | integer | Distance from the top. Content normally begins at `104`. |
| `w` | Yes | integer | Width. Standard widths: `760`, `373`, or `244`. |
| `h` | Yes | integer | Height. The bottom must not exceed `1030`. |
| `title` | No | string | Section heading inside the colored header row. |
| `color` | No | string | `sage`, `lav`, `blue`, `warm`, `rose`, or `ivory`. |
| `content` | Yes | object | Response-area definition selected by `type`. |

Use 14 px gaps between neighboring blocks; the validator warns when neighbours are closer. Blocks must be at least 180 × 92 px, stay within x=28–788 and y=104–1030, and must not overlap.

## Shared content fields

All content objects accept `type`, which defaults to `lines`, and an optional short, unique `prompt`.

## Content types

### `lines`

Open writing space.

```json
{"type": "lines", "prompt": "What does verse 3 say the shepherd does?", "rows": 8}
```

`rows` defaults to `6`.

### `checklist`

```json
{"type": "checklist", "items": ["Shepherd", "Pastures"], "blank_rows": 4}
```

`items` supplies labels; `blank_rows` adds unlabeled checkbox rows.

### `choices`

```json
{"type": "choices", "control": "radio", "options": ["New to me", "Heard it", "Know it"], "lines_after": 2}
```

`radio` creates one-choice circles; other `control` values use checkboxes. `lines_after` adds writing lines.

### `callout`

```json
{"type": "callout", "text": "Read the whole psalm before you begin.", "rows": 4}
```

`text` supplies guidance and `rows` adds optional writing space.

### `passage`

Scripture quoted from the NASB 2020, the one translation the tool prints. The engine adds the translation's name beside the reference.

```json
{
  "type": "passage",
  "reference": "Psalm 23:1-3",
  "verses": [{"number": 1, "text": "Text of the verse."}, {"number": 2, "text": "Text of the next verse."}],
  "notice": "The publisher's copyright notice, copied from lockman.org.",
  "rows": 0
}
```

`reference` and `verses` are required, and each verse needs a whole `number` and its `text`. `notice` prints under the text; a set that quotes Scripture with no notice draws a warning, since the notice may be printed elsewhere in the work. `rows` adds writing lines. A set quoting more than 500 verses is an error. A verse quoted twice counts twice.

### `table`

```json
{
  "type": "table",
  "rows": 7,
  "columns": [
    {"label": "Reference", "width": "18%"},
    {"label": "Who", "width": "18%"},
    {"label": "Notes"}
  ]
}
```

Each column accepts `label` and an optional `width` as a percentage or `px`, `em` or `rem` length; anything else is an error. `rows` defaults to `10`.

### `split`

```json
{
  "type": "split",
  "left": {"type": "lines", "prompt": "What the text says", "rows": 5},
  "right": {"type": "lines", "prompt": "What it asks of me", "rows": 5}
}
```

`left` and `right` are complete nested content objects.

### `custom_html`

```json
{"type": "custom_html", "html": "<div class=\"callout\">Custom content</div>"}
```

HTML is inserted without escaping. Use only trusted specifications. The author is responsible for safe markup and visual fit.

## Validation

Errors, which stop generation, cover a missing or malformed `pages` list, page and block shape, numeric geometry, safe-area bounds, minimum block size, overlaps, unknown content types, row counts that are not whole numbers from 0 to 200, malformed table columns, themes that are not colours, widths that are not lengths, and repeated concepts, a malformed passage, and more than 500 quoted verses. Warnings, which do not, cover a page with no blocks, an underfilled page, repeated section titles, repeated prompts, content estimated taller than its block, a title longer than the header shows, neighbouring blocks closer than 14 px, and quoted Scripture with no notice.

| Exit code | Meaning |
|---:|---|
| `0` | Generation succeeded, even if warnings were printed, or `--validate-only` passed without findings. |
| `1` | Validation completed with advisory warnings. |
| `2` | Invalid input, validation error, or unreadable specification. |

## Complete examples

- [`shared/examples/study/spec.json`](../shared/examples/study/spec.json) — one session of a study
- [`shared/study_spec_template.json`](../shared/study_spec_template.json) — reusable template

Also read [`CONTENT_GUIDE.md`](CONTENT_GUIDE.md) and [`DESIGN_STANDARD.md`](DESIGN_STANDARD.md).
