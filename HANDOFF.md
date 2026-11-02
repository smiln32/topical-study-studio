# Handoff

Written 2026-10-29, when the repository was laid out as an ICM workspace; brought up to date
2026-11-01. It holds the state of the work and what to do next. Why things are the way they
are is in [`DECISIONS.md`](DECISIONS.md).

## State

- The repository lives at `github.com/smiln32/topical-study-studio`, public, created
  2026-10-30 as `stg-planner-pages` and renamed 2026-11-01; the old address redirects.
  `main` matches the remote and CI passed on it; `git log` carries the hash. The branch
  `handoff-after-rename` is open with the work described under the review below.
- The ICM structure is in place and `tests/test_stages.py` holds it. The walk in
  `records/icm-audit.md` passes.
- One planner has been taken through the five stages, in the cold walk of 2026-11-01
  described below. The walk ended partway through a page-change revision, so on the owner's
  disk `vegetable-garden.brief.md` and `vegetable-garden.plan.md` sit in the stage 01 and 02
  `output/` folders and the first run's specification, check and export sit under
  `output/archive/2026-11-01/` in stages 03 to 05. It was a test of the structure, not a
  product; do not carry it on, and move the two files into the archive if the stage folders
  should be clean before the first study. All of it is ignored by git, and a fresh clone's
  `output/` folders hold only `.gitkeep`.
- The engine is unchanged in behaviour but for one fix: the overlap check in
  `study_factory.py` raised `TypeError` on a numeric string coordinate such as `"28"`
  instead of reporting a finding. It now parses geometry once and compares integers, with a
  test. The suite is twenty-three checks. CI compiles `study_studio.py` as well, reads the
  examples from `shared/examples/`, and carries the product's new name.
- An independent review on 2026-10-29 found seven gaps in the contracts: no way for stage
  05 to know the checked specification was the exported one, stale downstream files on a
  revision, stage 04 missing the inputs its report needs, an undefined warning note in
  stage 03, a wrong relative path in the report template, and two document claims. All
  seven are corrected. A second read found two more, also corrected: stage 04 took its
  verdict from generation, which exits 0 even with warnings, and a clean revision could
  leave an old warning note for stage 04 to read. The export gate is still contract-only.
- A review of the root files on 2026-10-30 corrected three documents: `HOW_IT_WORKS.md`
  said exit code 1 meant warnings, when only `--validate-only` returns it and plain
  generation exits 0 with warnings printed; the export contract was the one stage with no
  sensitive-topics line, so `CLAUDE.md`'s "every stage says so" was untrue; and
  `RIGHTS_AND_ATTRIBUTION.md` named Perplexity, which nothing else mentioned. The four
  pictures in `assets/design/` are now cited from `_config/design-system.md`. Two local
  tags, v2.0.0 and v2.1.0, were left over from the old repository's history and were
  deleted; the remote has v1.0.0 and v1.1.0 only, matching the code.
- On 2026-10-31 `_config/design-system.md` and `studio/styles.css` were reconciled. The
  stylesheet's canvas went to `#ececec`, the value the document, the palette specimen and
  the page engine share; its literal colours became tokens; two near-duplicate blues and
  two greens collapsed into one each; and the preview footer took the engine's `#8c8c8c`.
  The document gained the tokens the Studio needed (`ink-soft` corrected, `chrome-soft`,
  `surface-soft`, `focus`, `sage-deep`, `error`), a hero type level, the real button and
  input sizes, and a note that the page preview's colours belong to the engine.
  `tests/test_design_tokens.py` fails if the stylesheet uses a colour the token table does
  not name, or names one nothing in `studio/` uses.
- On 2026-10-31 every Canva reference was removed. The deliverable is now a PDF printed from
  the browser; the HTML is the generation format and stays editable. The
  `data-document-role="page"` marker on each section stays because the tests and CI count
  pages by it.
- The product is pivoting to topical Bible studies quoting the NASB 2020; `DECISIONS.md`
  records the terms and `README.md`, `CLAUDE.md` and `HOW_IT_WORKS.md` describe the
  direction. The stage contracts, `references/`, `shared/` and the Studio still speak only
  of planners, which is accurate until the study build exists. No study has been briefed.
  Doctrinal review was proposed and the owner declined it as a rule; do not add it to
  `CLAUDE.md` or the contracts.
- On 2026-10-31 the owner named the product **Topical Study Studio**. The engine is now
  `study_factory.py`, the server `study_studio.py`, the test file
  `tests/test_study_factory.py`, and "Planner Studio" and "STG Planner Pages" are gone from
  every file. The browser's saved-draft key is unchanged so existing drafts still open. The
  repository was renamed on GitHub on 2026-11-01 and its URLs updated, and the folder on disk
  was renamed to `topical-study-studio` the same day; nothing inside depends on either name.
  The repository description on GitHub still reads "STG Planner Pages: printable,
  Canva-importable planner pages from a JSON specification" and is the owner's to change in
  the repository settings.
- On 2026-11-01 Muse delivered a read-only review of `main` at 2343983: pass with
  non-blocking findings. The branch `handoff-after-rename` closes findings 1 to 6 and 8: the
  validator now rejects malformed shapes and unusable content instead of crashing, the Studio
  escapes theme, colour and geometry, themes and column widths must be colours and lengths,
  content taller than its box and blocks closer than 14 px draw warnings, `custom_html` is
  announced at generation time, and the documentation drift is gone. Finding 7, that no tool
  enforces the export gate, is the recorded decision. Finding 9 is item 5 under Next.
- On 2026-11-01 the cold walk was run: a fresh assistant given only "Make me a planner
  about starting a vegetable garden" and nothing else, with the owner's answers relayed at
  the gates. It routed itself to stage 01, stopped at every gate, left six brief fields
  `TO DECIDE` and asked, never ticked **Approved for export**, caught a one-word edit made
  to the specification after approval by the hash and refused to export, and on a page
  change archived stages 03 to 05 before going back to the brief. The contracts held. Two
  small gaps it exposed are closed: the router now sends a change of page count or
  must-include back to stage 01, and the check report names the blocks where a clipped row
  would show first. Enforcing the export gate in code is no longer on the list.

## Next

1. **The first study, through the stages as they are.** Give stage 01 a real study, six
   sessions on one subject, and take it through stage 02 only. The plan will show which
   pages the current blocks cannot express and how the whole-set uniqueness rule objects to
   a session shape that repeats. The engine changes in item 2 should come out of that plan,
   not out of a list.
2. **The study build**, in the order the first study demands:
   uniqueness per session rather than per set; the study content types (a passage with
   observation space, a cross-reference table, a memory-verse card, numbered discussion
   questions, a prayer page), each added to the engine, `references/SPECIFICATION.md` and an
   example; a study content guide, observation then interpretation then application; a verse
   count in stage 04 that fails above 500 and reports the proportion of the work that is
   Scripture; the NASB 2020 notice printed by stage 05, with the wording copied from
   lockman.org once; and a study example in `shared/examples/` to stand beside or replace the
   wellness ones. `shared/examples/study/` is a start: one session on Psalm 23 built from the
   planner types, made 2026-11-01 as the source of the README image. It quotes no Scripture,
   so it needs no notice; a full study example still waits on the study types.
3. **The page engine and the page standard disagree on two colours.**
   `references/DESIGN_STANDARD.md` gives block borders as `#606864` and rules as `#aeb7b2`;
   `study_factory.py` draws them `#5c5c5c` and `#b9b9b9`, and the Studio preview copies
   the engine. Change the standard or the engine, not the Studio. Changing the engine alters
   every generated page and the approved reference HTML in `shared/examples/`, so if the
   engine moves, regenerate those and look at them.
4. **Small cosmetic items**, none blocking: `--init` without `--topic` titles the page
   "My My Focus"; `study_studio.py` accepts `--host 0.0.0.0` with no authentication and
   its help text does not say so.
5. **Decide on a per-passage accuracy tick.** The review of 2026-11-01 asked that, before the
   first study quotes Scripture, stage 04 carry a line the author ticks per passage, "reference
   checked against the NASB 2020 text". That is accuracy, not doctrine, so it does not reopen
   the doctrinal-review decision; whether it goes in the contract is the owner's call.
