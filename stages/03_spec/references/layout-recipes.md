# Layout recipes

Block positions that sit on the grid `references/DESIGN_STANDARD.md` defines. Content runs
from y=104 to y=1030, with 14px between neighbours. Pick a recipe per page from the plan's
composition column, then set each block's `h` so the last row ends between 980 and 1030.

## Columns

| Layout | Widths | x positions |
|---|---|---|
| Full width | 760 | 28 |
| Halves | 373, 373 | 28, 415 |
| Thirds | 244, 244, 244 | 28, 286, 544 |
| Two-thirds and a third | 502, 244 | 28, 544 |
| A third and two-thirds | 244, 502 | 28, 286 |

## Rows

Stack rows top down. The next row's `y` is the previous row's `y + h + 14`.

| Composition | Rows |
|---|---|
| Full-width | One or more full-width blocks |
| Split | A full-width opener, then halves, then a full-width close |
| Three-column | A full-width opener, then thirds, then a full-width close |
| Stepped | Three or four full-width blocks of growing height, numbered in their titles |
| Asymmetric-but-aligned | Two-thirds beside a third, then a third beside two-thirds |

## Worked example: split, four blocks

| Block | x | y | w | h | Ends at |
|---|---|---|---|---|---|
| Opener | 28 | 104 | 760 | 150 | 254 |
| Left | 28 | 268 | 373 | 300 | 568 |
| Right | 415 | 268 | 373 | 300 | 568 |
| Close | 28 | 582 | 760 | 448 | 1030 |

This is `shared/planner_spec_template.json`. Every block is at least 180 x 92, and no two
overlap, which is what the validator checks.

## Row counts that fit

A `lines` row is 22px, a checklist row 24px, a table row about 40px with its header. Each
block loses 32px to its header and 22px to padding, and a prompt costs about 17px more.
Rows that do not fit are clipped; the validator estimates when that will happen and warns, so count before you write.
