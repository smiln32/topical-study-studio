# Handoff

Written 2026-10-29, when the repository was laid out as an ICM workspace; brought up to date
2026-11-04. It holds the state of the work and what to do next. Why things are the way they
are is in [`DECISIONS.md`](DECISIONS.md).

## State

**The product makes studies only, since 2026-11-04.** The entries below are a dated record; where
one speaks of planners, examples or files that are now gone, it describes that day.

- The repository lives at `github.com/smiln32/topical-study-studio`, public, created
  2026-10-30 as `stg-planner-pages` and renamed 2026-11-01; the old address redirects.
  `main` matches the remote and CI passed on it; `git log` carries the hash. No branch is
  open: `handoff-after-rename`, described under the reviews below, was merged 2026-11-03.
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
  test. The suite is thirty-eight checks. CI compiles `study_studio.py` as well, reads the
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
- On 2026-11-03 the first study went through stages 01 and 02 and stopped at the stage 02
  gate. It is *Timothy: Young and Trusted*, slug `timothy`: a led class of adults at church,
  30 minutes a session, six sessions of two pages, teacherly with a slant toward
  conversational, default colour, not sensitive, and the outcome in the owner's words,
  "understand youth can still be powerful". The approved brief is
  `stages/01_brief/output/timothy.brief.md` and the plan, not yet approved, is
  `stages/02_pages/output/timothy.plan.md`; both are git-ignored and exist on the owner's
  disk only. The plan chose the passages (Acts 16:1-5; 1 Timothy 4:12-16; Philippians
  2:19-24; 2 Timothy 1:3-7; 2 Timothy 2:1-7 with 1 Corinthians 16:10-11; 2 Timothy 4:1-8
  with Hebrews 13:23), 39 verses in all, and passes the stage's four audit checks. It did
  the job the handoff asked of it: every page can be laid out with today's blocks, but it
  names six shortfalls, in the order they bite: no passage block, so a callout stands in
  with no verse numbers, reference line or notice; the whole-set uniqueness rule refusing a
  section title that every session needs; no numbered discussion questions; no memory-verse
  card; no timeline; no support map. Item 2 under Next is reordered to match.
- On 2026-11-01 Muse delivered a read-only review of `main` at 2343983: pass with
  non-blocking findings. The branch `handoff-after-rename` closes findings 1 to 6 and 8: the
  validator now rejects malformed shapes and unusable content instead of crashing, the Studio
  escapes theme, colour and geometry, themes and column widths must be colours and lengths,
  content taller than its box and blocks closer than 14 px draw warnings, `custom_html` is
  announced at generation time, and the documentation drift is gone. Finding 7, that no tool
  enforces the export gate, is the recorded decision. Finding 9 is item 5 under Next.
  Codex reviewed the branch on 2026-11-03 and returned seven follow-ups, all closed on it the
  same day: whole-number row counts capped at 200, a JSON error from the Studio on failure,
  the clipping estimate corrected against Chrome, a real colour check, and two document lines.
- On 2026-11-01 the cold walk was run: a fresh assistant given only "Make me a planner
  about starting a vegetable garden" and nothing else, with the owner's answers relayed at
  the gates. It routed itself to stage 01, stopped at every gate, left six brief fields
  `TO DECIDE` and asked, never ticked **Approved for export**, caught a one-word edit made
  to the specification after approval by the hash and refused to export, and on a page
  change archived stages 03 to 05 before going back to the brief. The contracts held. Two
  small gaps it exposed are closed: the router now sends a change of page count or
  must-include back to stage 01, and the check report names the blocks where a clipped row
  would show first. Enforcing the export gate in code is no longer on the list.

- On 2026-11-04 the **study starter** was added on the branch `study-starter`:
  `studio/study-starter.html` and `studio/study-starter.js`, linked from the Studio's brief
  page and served by `study_studio.py` at `/study-starter.html`. It is a fill-in-the-blanks
  form: study title, brand, audience, page colour, then one session per passage with the
  reference, a title, up to ten words to look up, the read, observe, interpret, apply and
  prayer prompts (filled with wording that names the passage when left blank, so nothing
  repeats across sessions), and up to four discussion questions for a second page. It lays
  each session out on the split recipe with row counts computed from the engine's height
  estimate, checks through `/api/validate`, previews through `/api/render` in a sandboxed
  frame, and downloads the finished HTML or the JSON. The form is saved in the browser.
  `tests/test_study_starter.py` (eight checks at first, twelve now) serves the page and, when
  Node is present as it is on CI's runner, builds a three-session sample with the page's own
  function and asserts the validator returns nothing. `DECISIONS.md` records why it is a
  page beside the Studio rather than a mode in it. The starter writes planner content types
  and at first quoted no Scripture; the `passage` entry below changed that. `README.md`, `HOW_IT_WORKS.md` and the
  router describe it. Codex reviewed the commit the same day and returned seven findings, four
  blocking, all closed on the branch: a session titled like its own discussion page collided
  with it on concept (the concepts now carry "study" and "discussion" where a typed title
  cannot reach); two sessions on one passage repeated the generated title and prompts (the
  defaults now add the session number when a reference is shared, and an unedited default
  counts as blank); a storage failure left the page saying Saving… (it now says Not saved and
  tells the user to download the JSON); a 500 from the validator showed as a clean pass (the
  page now checks the status and the payload's shape); a saved draft of the wrong shape
  stopped the page loading (drafts are adopted field by field); page titles were forced
  upper case against the design standard (casing is kept); and the specification display
  fell back to a monospace face (it inherits). The suite is fifty checks.

- On 2026-11-04, on the branch `engine-clipped-lines` stacked on `study-starter`, the engine
  stopped cutting off writing lines. `.grid-lines` was 100% of a block body with a prompt above
  it, so the last line could fall outside the box: 2 lines on the Psalm 23 example. The body is
  now a flex column and writing lines share the height left under the prompt, in plain lines,
  callouts and both sides of a split. Those rules apply only to engine-drawn blocks;
  `custom_html` sits in a `.custom` wrapper and keeps its old sizing. `tests/test_print_fit.py`
  measures this in Chrome, including that custom lines do not collapse, a mistake the first
  attempt made. The basic, study and depression outputs were regenerated;
  `approved-reference.html` stays frozen.

- On 2026-11-04, on the branch `passage-block` stacked on `engine-clipped-lines`, the first study
  type arrived: a `passage` block with a reference line, verse numbers, an optional `notice` and
  optional writing rows. The engine prints the name NASB 2020 itself, so a block cannot name
  another translation. The validator rejects a malformed passage and more than 500 verses in a
  set, and warns when a set quotes Scripture with no notice. The study starter takes pasted text
  and a notice, and grows the block as the rows below shrink. No Scripture is in the repository;
  tests use placeholder text. The notice wording is not in the code: see item 0 under Next.
  The suite is sixty-eight checks. The real form was also driven in headless Chrome by a
  throwaway script, not kept in the repository: sixteen interactions passed with no page
  errors, covering prompts, the check, reordering, preview, reload, Start over, a bad draft
  and a refused save.

- On 2026-11-04, on the branch `studies-only` stacked on `passage-block`, the owner's decision
  "no planners" was carried out. Removed: the ADHD, basic and depression examples, the planner
  template and the page-ideas prompt, all kept in git history. The engine tests read
  `tests/fixtures/engine_spec.json`; `shared/study_spec_template.json` and `--init` write a study
  session; CI validates the study example and template. The Studio has ten study patterns, each
  held to the validator by a test, and drafts save under `studyStudio`, so an old planner draft
  stays in the browser unread. `references/CONTENT_GUIDE.md` is now the study content guide. The
  stages, references, chatbot prompt and root documents speak of studies, and stage 03 forbids
  typing a verse from memory. The brief and plan of the vegetable-garden test run moved into
  their stages' `output/archive/2026-11-01/`, on the owner's disk only. The suite is seventy-one
  checks, and the real Studio and starter were driven in headless Chrome by throwaway scripts.
  The Timothy brief and plan are untouched and still wait at the stage 02 gate.

## Next

0. **Check the Scripture terms against the publisher's page; the owner decides.** Lockman's
   page, https://www.lockman.org/permission-to-quote-copyright-trademark-information/, marked
   modified 2026-10-29 and read 2026-11-04, differs from what `CLAUDE.md`, `DECISIONS.md` and
   the README record. It allows up to 1,000 verses, where this repository says 500; the engine
   keeps 500, which stays inside the limit. It adds two conditions that nothing here checks: the
   verses may not amount to a complete book of the Bible, and may not exceed 50% of the work's
   text. Its notice lists 1960, 1971, 1977, 1995, 2020 and says to use only the last year
   corresponding to the edition quoted, with the example that a 1995 quotation leaves out 2020.
   That reads as keeping the earlier years up to the edition, where this repository says cite
   2020 alone, so ask Lockman or decide before printing a notice. Certain not-for-sale print
   material, such as church bulletins, may use the abbreviation (NASB) alone; whether a class
   handout qualifies is also a question for the owner or Lockman.

1. **Read the Timothy plan and decide.** The first study, *Timothy: Young and Trusted*, has
   been through stages 01 and 02 and waits at the stage 02 gate; see the State bullet. The
   owner reads `stages/02_pages/output/timothy.plan.md`, changes the page list as wanted,
   and chooses: build the engine changes in item 2 first and then run stage 03 with real
   study blocks, or run stage 03 now with the approximations the plan names and record them
   in its warnings file. The first is the better order; the plan exists so the engine can be
   changed for a real page list, not a list of guesses.
2. **The study build**, in the order the Timothy plan demands:
   the passage block, built 2026-11-04 and now to be used on its twelve pages; uniqueness per session rather than per set, since the
   validator will refuse "Read the passage" twelve times; numbered discussion questions,
   which a led class needs on most pages; a memory-verse card; a timeline and a support
   map, each wanted once; and, not demanded by this plan but still expected, a
   cross-reference table and a prayer page. Each type is added to the engine,
   `references/SPECIFICATION.md` and an example; a study content guide, observation then interpretation then application; a verse
   count in stage 04 that fails above 500 and reports the proportion of the work that is
   Scripture; the NASB 2020 notice printed by stage 05, with the wording copied from
   lockman.org once; and a fuller study example in `shared/examples/`. `shared/examples/study/` is a start: one session on Psalm 23 built from the
   planner types, made 2026-11-01 as the source of the README image. It quotes no Scripture,
   so it needs no notice; a full study example still waits on the study types.
3. **The page engine and the page standard disagree on two colours.**
   `references/DESIGN_STANDARD.md` gives block borders as `#606864` and rules as `#aeb7b2`;
   `study_factory.py` draws them `#5c5c5c` and `#b9b9b9`, and the Studio preview copies
   the engine. Change the standard or the engine, not the Studio. Changing the engine alters
   every generated page, so if the engine moves, regenerate `shared/examples/study/output.html`
   and look at it.
4. **A small item**, not blocking: `study_studio.py` accepts `--host 0.0.0.0` with no authentication and
   its help text does not say so.
5. **Teach the Studio's editor the callout and split types.** `studio/app.js` draws and
   edits only lines, checklists and choices; a callout or a split shows as writing lines in
   the preview and the response-style control has no value for it. Once the editor draws
   both and offers them as response styles, the study starter can gain an **Open in the
   Studio** button that writes its specification to the Studio's saved draft, and the
   Studio's JSON download can stand in for the starter's. Until then the starter's JSON is
   edited by hand or taken through stage 03.
6. **Decide on a per-passage accuracy tick.** The review of 2026-11-01 asked that, before the
   first study quotes Scripture, stage 04 carry a line the author ticks per passage, "reference
   checked against the NASB 2020 text". That is accuracy, not doctrine, so it does not reopen
   the doctrinal-review decision; whether it goes in the contract is the owner's call.
