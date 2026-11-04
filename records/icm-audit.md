# Current ICM Structural Audit

**Audit date:** 2026-10-29
**Scope:** the repository after the build was written down as five ICM stages.
**Standard:** Interpretable Context Methodology, Jake Van Clief and David McDermott,
https://arxiv.org/abs/2603.16021, and the cold-agent walk used in the sibling workspace
`cw-planner-factory`.

This file is the authoritative structural audit. After a material change to the folder
structure, re-run the walk and replace it.

## The five layers

| Layer | Question | Where | Result |
|---|---|---|---|
| 0 | Where am I? | `CLAUDE.md` | **PASS** |
| 1 | Where do I go? | `CONTEXT.md` | **PASS** |
| 2 | What do I do? | `stages/NN_name/CONTEXT.md` | **PASS** |
| 3 | What rules apply? | `_config/`, `references/`, `shared/`, a stage's own `references/` | **PASS** |
| 4 | What am I working with? | `stages/NN_name/output/` | **PASS** |

## Cold-agent walk

### 1. Can a fresh agent determine the rules that govern its behaviour?

**PASS.** `CLAUDE.md` opens with where the agent is, a folder map, the rules for working in
the stage folders including the gate rule, the commands, and the rules that are not style.

### 2. Can the agent determine where a task belongs?

**PASS.** `CONTEXT.md` routes: making a study, changing the tool and finding something out
each have named destinations. It does no work itself.

### 3. Can the agent determine how to execute a stage?

**PASS.** All five stages hold a `CONTEXT.md` with one job, Inputs, Process, Outputs, a human
gate and the next stage. Every path a contract names exists. `tests/test_stages.py` holds
both.

### 4. Does each stage do one job?

**PASS.** Brief decides what the study is. Pages decides what each page is for. Spec
writes the file and makes it validate. Check judges and changes nothing. Export writes the
files and decides nothing.

### 5. Do stages hand over through plain files?

**PASS.** Markdown and JSON between every stage. The proof and the finished study are HTML,
which is text. No binary passes between stages.

### 6. Is every output an edit surface?

**PASS.** A person can open and change the brief, the plan and the specification before the
next stage runs, and each contract tells the agent to read the file again. The specification
also opens in Topical Study Studio.

### 7. Can the agent tell where a run stands from the filesystem?

**PASS.** A stage with no file for a run in its `output/` has not run. All five hold only
`.gitkeep` in a fresh copy, and git ignores what a run writes.

### 8. Is reference material separate from run state?

**PASS.** `_config/` holds what the product is, `references/` the format and the standards,
`shared/` the starter, the examples and the chatbot prompt, and each stage's `references/`
only what that stage needs. Nothing a run writes lands there.

### 9. Are root responsibilities separated without duplication?

**PASS.** `CLAUDE.md` owns behaviour, `CONTEXT.md` routing, each stage contract execution,
`DECISIONS.md` settled choices, `HANDOFF.md` state and next steps, `README.md` what the tool
is, and `HOW_IT_WORKS.md` how a person sets it up and uses it. The stage contracts route to
sections of `HOW_IT_WORKS.md` rather than repeat them.

### 10. Do the stages match the product?

**PASS.** The five stages are the five things a creator does in Topical Study Studio in the same
order: say what the study is, choose the pages, write and lay them out, check, export.

### 11. Are the gates real?

**PASS, with one gap.** Each contract stops for a person, and `CLAUDE.md` forbids chaining
stages even under an autonomous instruction. The export gate is not enforced by code; the
contract alone holds it. *Added 2026-11-01:* the cold walk below showed the contract is
enough; the assistant never touched the approval line, and enforcement has been dropped
from `HANDOFF.md`.

## Where the workspace departs from the paper, on purpose

- **The engine is not inside the stage folders.** `study_factory.py`, `study_studio.py`,
  `studio/`, `tests/` and `assets/` stay at the root. `DECISIONS.md` records the reason.
- **`README.md`, `HOW_IT_WORKS.md`, `DECISIONS.md` and `HANDOFF.md` are at the root, and
  `records/` holds this audit.** The paper names none of them. The router points at each.
- **A root `output/` folder exists** for the owner's scratch files. It is not a stage's
  output and the router says so.
- **Stage folders use an underscore** (`01_brief`), the paper's Figure 2 style, where the
  reference repository's conventions use a hyphen. The owner's standing choice.

## What this audit did not do

- **The walk was made by the author of the contracts, not by a stranger.** *Added
  2026-11-01:* a stranger has since walked it. A fresh assistant given one line took a
  planner through all five stages, stopped at every gate, was caught by the hash when the
  specification was edited after approval, and archived before a revision. The two gaps it
  exposed are closed; `HANDOFF.md` has the record.

## Structural counts

- Stages: **5**, numbered 01 to 05 with no gap
- Stage contracts missing a required section: **0**
- Paths named by a contract that do not exist: **0**
- Stage output folders holding anything but `.gitkeep`: **0**

## Structural result

**PASS.** A cold agent can move through the workspace in a clear hierarchy:

`CLAUDE.md (behaviour) -> CONTEXT.md (routing) -> stage CONTEXT.md (execution) -> named inputs and references -> output (state)`

## Re-walk, 2026-10-31

The product was renamed Topical Study Studio and the engine, server and test file took the
`study_` prefix. No folder moved. The walk was repeated: every layer and every question above
holds, every path a contract names exists, and `tests/test_stages.py` passes.

## Re-walk, 2026-11-04

The product became studies only. The planner examples, the planner template and the page-ideas
prompt were removed; `shared/` now holds `study_spec_template.json`, `examples/study/` and the
chatbot prompt. No stage folder moved. The walk was repeated: every layer and every question
above holds, every path a contract names exists, and `tests/test_stages.py` passes. The
cold-agent walk of 2026-11-01 ran on a planner, before this change; a fresh walk on a study has
not been made.
