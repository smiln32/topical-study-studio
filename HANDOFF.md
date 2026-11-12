# Handoff

Written 2026-10-29; brought up to date 2026-11-12. It holds the state of the work and what to
do next. Why things are the way they are is in [`DECISIONS.md`](DECISIONS.md).

## State

- **The product makes topical Bible studies and nothing else**, since 2026-11-04.
- **`main` is at `89ef656`, pushed 2026-11-12, and CI passed:** 83 tests on Ubuntu, none
  skipped, including the Chrome tests that measure printed fit and the Node tests that run the
  starter's layout. That run is the first on Linux, so the passage-fit estimate has now held
  under Linux fonts for the cases the tests cover. Print preview has still been checked only on
  the owner's Windows machine.
- **Merged:** the branches `study-starter`, `engine-clipped-lines`, `passage-block` and
  `studies-only`. They still exist locally and can be deleted. Codex reviewed every commit on
  them; the last review, of `d2a1954` and `89ef656`, passed with no findings.
- **What a person can use today:**
  - The study starter, `studio/study-starter.html`: a form that lays out one page per
    session, plus a discussion page when questions are given, and quotes pasted NASB 2020 text
    in a `passage` block. A passage too long for the session page gets pages of its own,
    never splitting a verse. The download refuses a study the validator says will not print.
  - The Studio, `studio/index.html`: ten study page patterns, edited block by block. Its editor
    cannot yet edit callout, passage or split blocks.
  - The five stages under `stages/`, for an assistant, rewritten for studies.
- **The first study waits at the stage 02 gate.** *Timothy: Young and Trusted*, slug
  `timothy`: six sessions of two pages for a led class of adults. The approved brief is
  `stages/01_brief/output/timothy.brief.md` and the unapproved plan
  `stages/02_pages/output/timothy.plan.md`, both on the owner's disk only. The plan's
  first shortfall, a passage block, is now built.
- **The vegetable-garden test run** is archived under each stage's
  `output/archive/2026-11-01/`, on the owner's disk only. Do not carry it on.
- **Not yet walked:** the cold-agent walk of 2026-11-01 ran on a planner. No fresh assistant
  has taken a study through the five stages.

## Next

Items 0 and 1 are the owner's to decide. The build order agreed with the owner on 2026-11-11
runs from item 2.

0. **Settle the Scripture terms.** Lockman's page,
   https://www.lockman.org/permission-to-quote-copyright-trademark-information/, marked
   modified 2026-10-29 and read 2026-11-04, differs from what this repository assumed. It
   allows up to 1,000 verses, where the engine stops at 500, which stays inside the limit. It
   adds two conditions nothing here checks: the verses may not amount to a complete book of the
   Bible, and may not exceed 50% of the work's text. Its notice lists 1960, 1971, 1977, 1995,
   2020 and says to use only the last year corresponding to the edition quoted, with the example
   that a 1995 quotation leaves out 2020; that reads as keeping the earlier years, where this
   repository said cite 2020 alone. Certain not-for-sale print, such as church bulletins, may
   use the abbreviation (NASB) alone; whether a class handout qualifies is a question for the
   owner or Lockman. Until this is settled, no notice wording goes into the code.
1. **Read the Timothy plan and decide.** Approve or change
   `stages/02_pages/output/timothy.plan.md`. Running stage 03 is better after item 2, because
   the validator still refuses a section title repeated across sessions.
2. **Uniqueness per session.** The validator checks section titles and prompts across the
   whole set, so every session that needs "Observe" is refused. Scope it to a session, define
   what a session is in the specification, then drop the "Session n ·" prefixes the starter
   adds as a workaround.
3. **Depth levels.** Agreed with the owner: every study follows the guidelines, and a study or
   a single session can go deeper.
   - Level 1, the guide: what the starter makes today.
   - Level 2, context: who wrote it, who first heard it, what was happening, key words. Needs
     a prose block in the engine, with a height estimate like the passage block's.
   - Level 3, backstory and history: narrative pages and a timeline, using the prose and table
     blocks.
   - Level 4, further Scripture: more passages, a cross-reference table, parallel passages.
   - The starter gains a level for the study and an override per session; the brief and plan
     templates gain a depth field; `references/CONTENT_GUIDE.md` gains a section per level,
     including that every historical claim needs a source the author trusts.
   - Where the deeper text comes from first, typed into the starter or drafted by an
     assistant in the stages, is not yet decided; typing it into the starter was recommended.
   - Start with fixed pages and a warning when text will not fit. Automatic continuation
     pages only if that proves annoying.
4. **The leader's edition, optional.** A study stands on its own. Leader guidance and
   expected answers are an optional layer on a session or question, printed only in a second,
   separate output the author chooses to generate. Nothing leader-only ever prints in the
   reader's copy, and a study with no leader material is complete.
5. **Other add-ins:** numbered discussion questions as their own block type, a memory-verse
   card, a support map, a cover page and contents, a closing review page.
6. **Images, later.** An image block embedded in the HTML, with a caption and a rights line.
   Print resolution and rights need settling first.
7. **Decide what the Studio is for.** Either teach its editor the callout, passage and split
   blocks, so it can open and refine what the starter writes, or treat the starter as the
   product. Teaching the editor was recommended. Its ten patterns and the starter's default
   prompts are an assistant's wording: the owner should read them and change anything not in
   their voice.
8. **Scripture checks that wait on item 0:** stage 04's report recording the verse count and
   the share of the work that is Scripture; checks for a complete book and the 50% condition;
   stage 05 printing the notice once its wording is settled.
9. **Decide on a per-passage accuracy tick.** The review of 2026-11-01 asked that, before the
   first study quotes Scripture, stage 04 carry a line the author ticks per passage, "reference
   checked against the NASB 2020 text". That is accuracy, not doctrine, so it does not reopen
   the doctrinal-review decision; whether it goes in the contract is the owner's call.
10. **The page engine and the page standard disagree on two colours.**
    `references/DESIGN_STANDARD.md` gives block borders as `#606864` and rules as `#aeb7b2`;
    `study_factory.py` draws `#5c5c5c` and `#b9b9b9`, and the Studio preview copies the engine.
    Change the standard or the engine, not the Studio; if the engine moves, regenerate
    `shared/examples/study/output.html` and look at it.
11. **Small:** `study_studio.py` accepts `--host 0.0.0.0` with no authentication, and its help
    text does not say so. The merged branches listed under State can be deleted.

## Record

Dated entries, oldest first. Each describes the repository on its day; where one speaks of
planners, examples or files now gone, it is history.

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
- On 2026-10-31 the product began pivoting to topical Bible studies quoting the NASB 2020; `DECISIONS.md`
  records the terms and `README.md`, `CLAUDE.md` and `HOW_IT_WORKS.md` describe the
  direction. The stage contracts, `references/`, `shared/` and the Studio still speak only
  of planners, which is accurate until the study build exists. No study has been briefed.
  Doctrinal review was proposed and the owner declined it; `DECISIONS.md` records it.
- On 2026-10-31 the owner named the product **Topical Study Studio**. The engine is now
  `study_factory.py`, the server `study_studio.py`, the test file
  `tests/test_study_factory.py`, and "Planner Studio" and "STG Planner Pages" are gone from
  every file. The browser's saved-draft key is unchanged so existing drafts still open. The
  repository was renamed on GitHub on 2026-11-01 and its URLs updated, and the folder on disk
  was renamed to `topical-study-studio` the same day; nothing inside depends on either name.
  The owner has since changed the repository description on GitHub.
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
  enforces the export gate, is the recorded decision. Finding 9, the per-passage accuracy tick, is now item 9 under Next.
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

- On 2026-11-10 Codex reviewed the stack from `cb9a65a` to `9a51c03`: fail, eight findings.
  All are closed on `studies-only`, with a regression test each. A long passage could silently
  drop words to look up or push blocks below the page; every word is now kept and a passage too
  long for the session page gets a page of its own. Pages added past the Studio's ten patterns
  repeated a concept; they are now numbered. The passage height ignored a wrapping reference;
  it is counted, and long words wrap. References differing only in punctuation were not seen
  as shared; the starter now normalises as the validator does. Verse numbers such as "²" and
  over-long digit strings crashed validation, and so did row counts, which Codex did not
  report; both are findings now. A passage block 28 px wide divided by zero; it is reported.
  Passages and custom HTML outside a split's sides were counted though never drawn; only a
  split's sides are walked now. Codex's re-review on 2026-11-11 found two left: a passage longer than
  a whole page still clipped, and removing then adding a Studio page could repeat a concept. A long
  passage now continues across as many pages as it needs, a verse never split, and the starter
  refuses to download HTML the validator says will not print; an added page takes the first
  identity no page has. Codex's third review, of `98fa869`, found the guard could check one
  specification and download another edited while the check was pending; the download now
  takes one snapshot for both. The read instruction also says "pages" when the passage spans
  several. Codex could not launch Chrome, so print preview, Linux fonts
  and nested custom layouts are still unverified outside this machine.
