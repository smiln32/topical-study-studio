# Full-Page Planner Design Standard

## Canvas and geometry

- US Letter: exactly 816 x 1056 px; white print surface.
- Outer content edges: x=28 and x=788. Header y=24–90. Content y=104–1030. Footer stays below content.
- Use a 3-unit horizontal grid with 14 px gutters: full 760 px, halves 373 px, thirds 244 px (allow one-pixel rounding).
- Use 14 px vertical gaps. Align every box edge to another edge or the outer grid.
- Fill the page deliberately, not mechanically. Writing space is content; accidental voids are not.
- Never overlap blocks or mix manual and automatic placement on one page.

## Typography

- Display titles: Georgia (serif, with Times New Roman fallback), 23 px, bold, balanced, never all-caps by default.
- UI and writing prompts: Aptos/Helvetica Neue/Arial, 8.5–11 px depending on role.
- Section heads: sentence case, 10.5–11 px, bold. Avoid tracked uppercase scaffolding.
- Use no more than two type families. Keep contrast high and never use pale gray for instructional text.
- Headings must fit without clipping; shorten copy before shrinking below the minimum sizes.

## Visual system

- Ink #343a38; borders #606864; rules #aeb7b2; white background.
- Sage #b2c6b1 / #dfe9df; lavender #c6b5c8 / #e8dfea; slate #7b9fb3 / #dce8ee; blush #e6d7d3 / #f0e6e2.
- Use color to group and orient, not decorate. One dominant page theme plus restrained supporting fills.
- Complete 10–12 px corners, consistent 1.15–1.2 px borders, no shadows, gradients, textures, or clipped decoration.
- Everything is text, borders and tables; no page is a flattened image.

## Page composition

Each page has one named `concept`. Choose a composition that expresses it: a tracker can be tabular; a decision can split; a sequence can step; a reflection can be spacious. Do not reuse the same block silhouette on adjacent pages. Rotate full-width, split, three-column, stepped, and asymmetric-but-aligned arrangements.

Read `CONTENT_GUIDE.md` before writing prompts. Use `custom_html` only when supported types cannot express the interaction.

## Required checks

- Exact canvas and safe bounds.
- No collisions; minimum block size 180 x 92 px.
- Content reaches y=980–1030 unless whitespace is intentionally documented.
- No repeated page concepts, section titles, or prompts.
- Text fits at print size; writing areas are practically usable.
- Correct page count verified in print preview.
- Health-related content includes appropriate scope language and professional review before sale/publication.
