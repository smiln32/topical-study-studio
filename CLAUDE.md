# Instructions for Claude

**Where am I?** In Topical Study Studio: software that turns a JSON specification into
printable US Letter pages, printed to PDF from a browser. It builds planners today and is
being turned into a tool for topical Bible studies. The study content types do not exist
yet, so until they do the stages build planners as written. `study_factory.py` is the
engine, `studio/` is Topical Study Studio, the browser application, and `stages/` is the same
build laid out as five folders an assistant can walk one at a time.

This workspace follows the Interpretable Context Methodology (ICM) of Jake Van Clief and
David McDermott (https://arxiv.org/abs/2603.16021). This file is Layer 0. [`CONTEXT.md`](CONTEXT.md)
is Layer 1 and routes every task; read it next.

## What is where

```text
CLAUDE.md          Layer 0: where you are and the rules (this file)
CONTEXT.md         Layer 1: where a task goes
stages/            Layer 2: 01_brief, 02_pages, 03_spec, 04_check, 05_export
                   each holds CONTEXT.md (its contract), references/, output/
_config/           Layer 3: what the product is and how the Studio looks
references/        Layer 3: the specification, the page design standard, the content guide
shared/            Layer 3: the starter specification, the examples, the chatbot prompt
records/           Kept, not instructions: the ICM structure audit
study_factory.py study_studio.py studio/ tests/ assets/   the engine and its checks
DECISIONS.md       why things are the way they are
HANDOFF.md         what comes next
README.md          the public front page
HOW_IT_WORKS.md    how a person sets the tool up and uses it
RIGHTS_AND_ATTRIBUTION.md   who owns what and under which licence
```

## Working in the stage folders

- **One stage, one job.** Do what the stage's `CONTEXT.md` says and nothing a later stage owns.
- **Read only what the stage names.** Its Inputs table is the whole of what you need.
- **Write only to that stage's `output/`.** To change an earlier stage's file, go back to
  the stage that owns it.
- **Stop at every human gate.** Finish one stage, report, and wait for the person to say
  "approved" before starting the next. Do not chain stages in one pass, even when told to
  work autonomously: that instruction means build without supervision, not skip the gates.
  Read the output file again before continuing; the person may have edited it.
- **Do not fill a gap with a guess.** If an input does not say, ask.
- **A stage's `output/` tells you where a run stands.** One holding only `.gitkeep` has not run.

## Commands

Run from the project root.

```bash
python -m unittest discover -s tests -v                       # the whole suite
python -m py_compile study_factory.py study_studio.py
python study_factory.py SPEC.json OUT.html --validate-only  # check a specification
python study_factory.py SPEC.json OUT.html                  # generate the pages
python study_factory.py --init FILE.json --topic "TOPIC"    # a starter specification
python study_studio.py                                      # the Studio at http://127.0.0.1:8765
```

No third-party Python packages. Python 3.9 is the floor; CI runs 3.12 only, so keep to 3.9
syntax yourself. There is no linter or formatter; do not add one without asking.

## Rules that are not style preferences

- **Restart the server after changing `study_factory.py`.** `study_studio.py` imports it
  and holds the old module in memory.
- **`custom_html` is inserted unescaped.** Only trusted specifications may use it, and the
  stage contracts prefer the standard content types for that reason.
- **The page geometry is fixed:** 816 x 1056, content x=28 to 788 and y=104 to 1030, 14px
  gaps. The constants live at the top of `study_factory.py` and `references/DESIGN_STANDARD.md`
  explains them. Change both or neither.
- **`study_studio.py` and `studio/app.js` are dense on purpose**, semicolon-joined and
  one-line. Do not reformat them.
- **Sensitive topics.** A planner or study about mental health, trauma, disability,
  medication, grief, addiction or crisis is flagged for professional review before
  publication. Every stage says so.
- **Scripture is the NASB 2020 only.** Quote from the New American Standard Bible 2020 (The
  Lockman Foundation), keep one work under 500 verses, and cite 2020 alone in the copyright
  notice. Do not quote or bundle any other translation, and do not paraphrase the notice:
  copy the publisher's wording once it is confirmed at lockman.org.

## Working style here

- Answer a question with an answer. Do not start editing until asked to.
- Never push to GitHub or open, edit or merge a pull request. Commit locally on a branch,
  report the hash and the verification, and stop.
- A claim belongs in one document. Before adding one, check it is not already made elsewhere.
- When something is left undone, write it into `HANDOFF.md`.
- After any change to the folder structure, re-run the walk in `records/icm-audit.md`.
