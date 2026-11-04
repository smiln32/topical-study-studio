# 03_spec/CONTEXT.md: Layer 2 · Stage Contract

**One job:** turn the plan into a study specification that validates cleanly.

This stage writes the JSON file the engine reads. Layout and wording both happen here,
because the validator judges them together.

## Inputs

| Layer | What | Where | Section |
|---|---|---|---|
| 4 (working) | The approved plan | `../02_pages/output/<slug>.plan.md` | Full file |
| 4 (working) | The brief, for the title, footer, tone and colour | `../01_brief/output/<slug>.brief.md` | Full file |
| 3 (reference) | The file format, field by field | `../../references/SPECIFICATION.md` | Full file |
| 3 (reference) | Standard block positions on the grid | `references/layout-recipes.md` | Full file |
| 3 (reference) | How a prompt should read | `../../references/CONTENT_GUIDE.md` | Prompt design, Content review checklist |
| 3 (reference) | The visual rules a page must obey | `../../references/DESIGN_STANDARD.md` | Canvas and geometry, Required checks |
| 3 (shared) | A specification to start from | `../../shared/study_spec_template.json` | Full file |

## Process

Run commands from the project root.

1. Start from the template. Set `set_title` and `footer_label` from the brief.
2. For each plan row, write one page: `concept` word for word from the plan, a `title` of
   about 22 characters, a one-line `subtitle`, the brief's `theme`, and blocks laid out on
   the recipe that matches the row's composition.
3. Write every prompt, section title, checklist item and option so that it is specific,
   answerable and used nowhere else in the set. Prefer the standard content types; do not use
   `custom_html` unless the plan names an interaction no type can express.
4. Quote Scripture only from text the person supplies, in a `passage` block. Never type a
   verse from memory; where there is no text, tell the reader where to read.
5. Fill each page to y=980 or lower without crossing y=1030. Writing space is content.
6. Validate, and fix every finding. A warning may stay only when fixing it would break the
   plan; then write `output/<slug>.warnings.md` with the warning word for word and why it
   stays. Stage 04 reads that file. When validation is clean, delete any `<slug>.warnings.md`
   an earlier run left; when the warnings change, rewrite it so it matches the validator.

   ```bash
   python study_factory.py stages/03_spec/output/<slug>.json stages/04_check/output/<slug>.proof.html --validate-only
   ```

   Validation writes no file. Exit code 2 is an error, 1 a warning, 0 clean.

## Audit

| Check | Pass condition |
|---|---|
| Validation | Exit code 0, or every remaining warning is in `output/<slug>.warnings.md` with its reason |
| Plan fidelity | One page per plan row, same order, same concepts |
| Sensitive topic | If the brief says yes, the named page carries the scope and support note |

## Outputs

| Artifact | Location | Format |
|---|---|---|
| The specification | `output/<slug>.json` | JSON, as `../../references/SPECIFICATION.md` describes |
| Warnings that stay, only if any | `output/<slug>.warnings.md` | Markdown: each warning word for word, then one line on why it stays |

## Human gate

The person may edit the file, or open it in Topical Study Studio and change it there. Do not start
stage 04 until they say it is ready.

## Next

`../04_check/CONTEXT.md`
