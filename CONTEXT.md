# CONTEXT.md: Layer 1 · Workspace Task Routing

> **Where do I go?** This file routes a task to the place that handles it. It does not do
> work. It points. Read `CLAUDE.md` first for the rules.

Topical Study Studio turns a planner idea into printable pages. The folders are the instructions.

| Layer | Question | Where |
|---|---|---|
| 0 | Where am I? | `CLAUDE.md` |
| 1 | Where do I go? | This file |
| 2 | What do I do? | The `CONTEXT.md` inside each stage folder |
| 3 | What rules apply? | `_config/`, `references/`, `shared/`, a stage's own `references/` |
| 4 | What am I working with? | The `output/` folder inside each stage |

## The planner build at a glance

One planner is one run through five stages. Each stage does one job, writes plain files to
its own `output/`, and stops for a person to read them before the next begins.

```text
01_brief ──▶ 02_pages ──▶ 03_spec ──▶ 04_check ──▶ 05_export
                             ▲            │
                             └── FAIL ────┘
```

| # | Stage | Does one job | Reads | Writes to its `output/` |
|---|---|---|---|---|
| 01 | `stages/01_brief` | Write down what the planner is | The person's request | `<slug>.brief.md` |
| 02 | `stages/02_pages` | Choose the page concepts and their order | The brief | `<slug>.plan.md` |
| 03 | `stages/03_spec` | Write the specification and make it validate | The plan, the brief | `<slug>.json` |
| 04 | `stages/04_check` | Decide whether it is fit to export | The specification | `<slug>.check.md`, `<slug>.proof.html` |
| 05 | `stages/05_export` | Produce the files to keep and import | The specification, the approved check | `<slug>.html`, `<slug>.json` |

Topical Study Studio does the same five steps on screen, by hand. The stage folders are how an
assistant does them, with the same engine and the same rules.

## Routing rules

**Making a planner**

- **"Make me a planner"** → `stages/01_brief/CONTEXT.md`. Begin there, every time.
- **"Carry on with the planner called X"** → look in each stage's `output/` for files named
  `X.*`, not counting anything under `output/archive/`. The last stage that holds one is
  where the run stands.
- **"Change the pages of X"** → `stages/02_pages/CONTEXT.md`, then run 03 to 05 again. If
  the change alters the page count or what the planner must include, it is a change to the
  brief: go to `stages/01_brief/CONTEXT.md` first, then 02 to 05.
- **"Change the wording or layout of X"** → `stages/03_spec/CONTEXT.md`, then 04 and 05 again.
- **Before either revision begins:** in every later stage, move the files named `X.*` from
  `output/` into `output/archive/<YYYY-MM-DD>/` (add `-2`, `-3` for another revision the same
  day). Then no stale check or export can pass for the current one, and the earlier export
  is kept.
- **"I want to make one by hand"** → run `python study_studio.py` and use the Studio.
- **"I want a study, quickly"** → run `python study_studio.py` and open `studio/study-starter.html`
  from it: fill in the sessions and it writes a specification that validates today.
- **"I am using a chatbot, not this folder"** → `shared/new-chat-starter-prompt.md`.

**Changing the tool**

- **"Change how a page prints"** → `study_factory.py`, held to `references/DESIGN_STANDARD.md`.
- **"Change the Studio"** → `studio/`, held to `_config/design-system.md`.
- **"Run or fix the tests"** → `tests/`.
- **"Add a content type"** → `study_factory.py`, then `references/SPECIFICATION.md`, then an example.

**Finding something out**

- **"What is the planner file format?"** → `references/SPECIFICATION.md`.
- **"How should a page look?"** → `references/DESIGN_STANDARD.md`.
- **"How should a prompt read?"** → `references/CONTENT_GUIDE.md`.
- **"Who is this for?"** → `_config/product.md`.
- **"What should I work on next?"** → `HANDOFF.md`.
- **"Why is it like this?"** → `DECISIONS.md`.
- **"How does a person use it?"** → `HOW_IT_WORKS.md`, written for people, not assistants.
- **"What is it?"** → `README.md`.

## Shared resources (Layer 3)

| Folder | What it holds |
|---|---|
| `_config/` | `product.md`, what Topical Study Studio is for; `design-system.md`, how it looks |
| `references/` | `SPECIFICATION.md`, the file format; `DESIGN_STANDARD.md`, the printed page; `CONTENT_GUIDE.md`, the words |
| `shared/` | The starter specification, the examples and the chatbot prompt; see `shared/CONTEXT.md` |
| A stage's own `references/` | Material only that stage needs |

## The engine

The stages do not contain the code that does the work. They call it.

| Where | What |
|---|---|
| `study_factory.py` | Validates a specification and turns it into pages |
| `study_studio.py` | The local server behind the Studio |
| `studio/` | The Studio |
| `assets/` | The README's pictures and the approved design references |
| `tests/` | The checks, including `test_stages.py`, which holds this structure |

## Human gates

A person reviews after **every** stage. Two gates are firm:

- **After 01:** the brief must be right before pages are chosen.
- **After 04:** nothing is exported until **Approved for export** is ticked in the check report.

## What is not routed

- `output/` at the root holds the owner's scratch files. It is ignored by git and is not a
  stage's output.
- `records/` holds what is kept but is not an instruction: the ICM structure audit.
