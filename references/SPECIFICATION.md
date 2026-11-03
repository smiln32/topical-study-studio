# Planner Specification Reference

Topical Study Studio reads a UTF-8 JSON document and renders each entry in `pages` as an editable 816 × 1056 px US Letter page.

## Create a starter file

```bash
python study_factory.py --init my-planner.json --topic "Morning Routine"
```

Then validate and generate it:

```bash
python study_factory.py my-planner.json output.html --validate-only
python study_factory.py my-planner.json output.html
```

## Top-level fields

| Field | Required | Type | Purpose |
|---|---:|---|---|
| `set_title` | No | string | HTML document title. Defaults to `Planner Set`. |
| `footer_label` | No | string | Left side of every page footer. Defaults to `Planner`. |
| `pages` | Yes | array | Ordered list of planner pages. At least one page is required. |

## Page fields

| Field | Required | Type | Purpose |
|---|---:|---|---|
| `concept` | Recommended | string | The page's single useful job. Must be unique across the set. |
| `label` | No | string | Page label, written to the page section as a `data-label` attribute. Defaults to the page title. |
| `title` | No | string | Main page heading. |
| `subtitle` | No | string | Short supportive explanation beneath the title. |
| `theme` | No | CSS color | Header color: a hex code such as `#b2c6b1`, a color name, or an `rgb()`/`hsl()` value. Anything else is an error. Defaults to `#b2c6b1`. |
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
{"type": "lines", "prompt": "What feels most useful now?", "rows": 8}
```

`rows` defaults to `6`.

### `checklist`

```json
{"type": "checklist", "items": ["Drink water", "Choose one priority"], "blank_rows": 4}
```

`items` supplies labels; `blank_rows` adds unlabeled checkbox rows.

### `choices`

```json
{"type": "choices", "control": "radio", "options": ["Low", "Steady", "High"], "lines_after": 2}
```

`radio` creates one-choice circles; other `control` values use checkboxes. `lines_after` adds writing lines.

### `callout`

```json
{"type": "callout", "text": "Small progress still counts.", "rows": 4}
```

`text` supplies guidance and `rows` adds optional writing space.

### `table`

```json
{
  "type": "table",
  "rows": 7,
  "columns": [
    {"label": "Day", "width": "18%"},
    {"label": "Energy", "width": "18%"},
    {"label": "Notes"}
  ]
}
```

Each column accepts `label` and an optional `width` as a percentage or `px`, `em` or `rem` length; anything else is an error. `rows` defaults to `10`.

### `split`

```json
{
  "type": "split",
  "left": {"type": "lines", "prompt": "More of", "rows": 5},
  "right": {"type": "lines", "prompt": "Less of", "rows": 5}
}
```

`left` and `right` are complete nested content objects.

### `custom_html`

```json
{"type": "custom_html", "html": "<div class=\"callout\">Custom content</div>"}
```

HTML is inserted without escaping. Use only trusted specifications. The author is responsible for safe markup and visual fit.

## Validation

Errors cover page/block presence and shape, numeric geometry, safe-area bounds, minimum block size, overlaps, unknown content types, row counts that are not whole numbers from 0 to 200, malformed table columns, themes that are not colours, widths that are not lengths, repeated concepts, repeated section titles, and repeated prompts. Warnings cover an underfilled page, content estimated taller than its block, a title longer than the header shows, and neighbouring blocks closer than 14 px.

| Exit code | Meaning |
|---:|---|
| `0` | Generation succeeded, even if warnings were printed, or `--validate-only` passed without findings. |
| `1` | Validation completed with advisory warnings. |
| `2` | Invalid input, validation error, or unreadable specification. |

## Complete examples

- [`shared/examples/basic/spec.json`](../shared/examples/basic/spec.json) — two-page introduction
- [`shared/examples/depression/spec.json`](../shared/examples/depression/spec.json) — full planner
- [`shared/planner_spec_template.json`](../shared/planner_spec_template.json) — reusable template

Also read [`CONTENT_GUIDE.md`](CONTENT_GUIDE.md) and [`DESIGN_STANDARD.md`](DESIGN_STANDARD.md).
