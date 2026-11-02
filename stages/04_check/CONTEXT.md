# 04_check/CONTEXT.md: Layer 2 · Stage Contract

**One job:** find out whether the planner is fit to export. Change nothing.

The validator sees geometry, repetition and, by estimate, content too tall for its box. It
cannot see a cramped writing area or a prompt that is not worth answering. This stage renders a proof and
writes down what a person must judge.

## Inputs

| Layer | What | Where | Section |
|---|---|---|---|
| 4 (working) | The specification | `../03_spec/output/<slug>.json` | Full file |
| 4 (working) | The brief, for the page count and the sensitive-topic flag | `../01_brief/output/<slug>.brief.md` | Page count, Sensitive topic |
| 4 (working) | The approved plan, for which page carries the scope and support note | `../02_pages/output/<slug>.plan.md` | Sensitive topic note |
| 4 (working) | Warnings stage 03 left standing, when the file exists | `../03_spec/output/<slug>.warnings.md` | Full file |
| 3 (reference) | The shape of the check report | `references/check-report-template.md` | Full file |
| 3 (reference) | What to look at in the browser | `../../HOW_IT_WORKS.md` | Reviewing generated pages |
| 3 (reference) | What a page must satisfy | `../../references/DESIGN_STANDARD.md` | Required checks |
| 3 (reference) | What a page's words must satisfy | `../../references/CONTENT_GUIDE.md` | Content review checklist |

## Process

Run the command from the project root.

1. Validate first. The verdict comes from this exit code, not from the next step's, because
   generation returns 0 whenever it writes a proof, warnings or not:

   ```bash
   python study_factory.py stages/03_spec/output/<slug>.json stages/04_check/output/<slug>.proof.html --validate-only
   ```

2. Render the proof. It prints the same findings again:

   ```bash
   python study_factory.py stages/03_spec/output/<slug>.json stages/04_check/output/<slug>.proof.html
   ```

3. Record the specification's SHA-256, so stage 05 can tell whether the file it exports is
   the file that was checked:

   ```bash
   python -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" stages/03_spec/output/<slug>.json
   ```

4. Copy `references/check-report-template.md` to `output/<slug>.check.md`. Record the hash,
   the validation exit code and every finding, word for word. If `<slug>.warnings.md`
   exists, copy each reason beneath its warning. From the brief and the plan, record the
   page count and the page that carries the scope and support note. From the specification,
   name the blocks with the most rows for their height: the validator estimates a clipped row
   but cannot see one, so the report says where one would show first.
5. Give a verdict from the validation exit code: **PASS** with 0; **PASS WITH WARNINGS** with
   1 when every warning has its reason from stage 03; **FAIL** with 2, with no proof written,
   or with a warning that has no reason.
6. On **FAIL**, go back to stage 03 and say what the report names. Do not edit the
   specification from this stage.
7. Leave the **Human review** list unticked. It is the person's to tick.

## Outputs

| Artifact | Location | Format |
|---|---|---|
| The check report | `output/<slug>.check.md` | Markdown, the template filled in |
| The proof | `output/<slug>.proof.html` | HTML, every page at true size |

## Human gate

The person opens the proof at 100% and in print preview, works through the Human review
list, and ticks **Approved for export** or sends it back. Stage 05 does not run until that
line is ticked.

## Next

`../05_export/CONTEXT.md`
