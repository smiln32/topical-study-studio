# Decisions

What has been settled and why. Read the relevant part before arguing with a decision. What to
do next is in `HANDOFF.md`.

## The product

**It is becoming a topical Bible study tool.** Decided by the owner 2026-10-31. As a
planner generator the repository was too close to the owner's sibling repository to keep
both. A study is a different product that the same engine, validator, Studio and stages can
serve: a set of sessions, each a few pages that take the reader through a passage and into
application. The brand already fits; STG is Simplify to Glorify. The study content types,
the per-session uniqueness rule and the study content guide are not built yet, so the stages
build planners until they are, and `README.md` says what is planned and what is not.

**It makes studies and nothing else.** Decided by the owner 2026-11-04. Planner support was
removed: the examples, the template, the page-ideas prompt and the Studio's planner patterns are
gone, and git history keeps them. The engine's block types stayed, because a study page uses all
of them. Where this file speaks of planners below, it is recording what was true when that
decision was made. The four pictures in `assets/design/` still show planner pages, and stay as
the record of the approved look.

**The product is Topical Study Studio.** Named by the owner 2026-10-31. The engine is
`study_factory.py`, the server `study_studio.py`, and the browser application is the Studio.
The names drop "planner" without binding the tool to one kind of study. The repository keeps
its GitHub name until the owner renames it there, so every URL still works. The browser's saved-draft key became `studyStudio` when planners were removed, so an old planner
draft is left in the browser, unread and not overwritten.

**Canva is gone; the deliverable is a printed PDF.** Decided by the owner 2026-10-31. The
product began as a Canva import tool. Studies are sold and printed as PDF, so every Canva
reference, workflow section and default title was removed. The engine still renders HTML,
because a browser's print dialog turns it into a US Letter PDF faithfully and the HTML stays
editable; the `data-document-role="page"` marker on each section stays because the tests
and CI count pages by it.

**Scripture is quoted from the NASB 2020 and nothing else.** Decided by the owner
2026-10-31. The New American Standard Bible 2020 (The Lockman Foundation) allows up to 500
verses in one work without written permission, and its notice must cite 2020 only. No other
translation is quoted or bundled. The exact notice wording and the policy's other conditions
are to be confirmed at lockman.org before the first study ships; stage 04 is to count the
verses and stage 05 to print the notice once the study build exists.

## The workspace

**This repository follows ICM, by choice.** Decided by the owner 2026-10-29. The workspace
follows the Interpretable Context Methodology of Jake Van Clief and David McDermott
(https://arxiv.org/abs/2603.16021), laid out the way the owner's sibling repository
`cw-planner-factory` already is, so an assistant moving between the two finds the same
shape. `CLAUDE.md` says where you are, `CONTEXT.md` routes, each stage's `CONTEXT.md` is its
contract, `_config/`, `references/` and `shared/` hold what is stable, and each stage's
`output/` holds what a run writes. Keep it so:

- A new step in the build is a new numbered stage with its own contract,
  `references/` and `output/`, not a script somewhere else.
- New reference material goes in `_config/`, `references/`, `shared/` or a stage's own
  `references/`, not at the root.
- After any change to the folder structure, re-run the walk in `records/icm-audit.md`.
  `tests/test_stages.py` fails if a stage loses its contract, a contract names a file that is
  not there, or the router stops naming a stage.

**Stage folders are `stages/NN_name/`, underscore, from 01.** The paper's Figure 2 style,
which the owner chose over the hyphenated `01-name` style on 2026-07-16 for all their
workspaces. The standalone ICM audit tool recognises only this dialect.

**The engine stays at the root.** `study_factory.py`, `study_studio.py`, `studio/`,
`tests/` and `assets/` did not move. The paper describes staged content work, not
application source, and keeping the engine where the commands, the tests and CI expect it
means the restructure changed no code path. The stages call the engine; they do not hold it.

**Five stages, matching the sibling.** `01_brief`, `02_pages`, `03_spec`, `04_check`,
`05_export`. The third is `spec` rather than the sibling's `edit` because here the assistant
writes the specification from the plan; there is no page library to build from.

**Moved documents keep their names.** `SPECIFICATION.md`, `DESIGN_STANDARD.md` and
`CONTENT_GUIDE.md` went to `references/` unrenamed so that links, history and the sibling's
`references/SPECIFICATION.md` still correspond. `PRODUCT.md` and `DESIGN.md` became
`_config/product.md` and `_config/design-system.md`, lower case like the sibling's
`_config/`, because they describe the Studio product rather than the printed page.

**`HOW_IT_WORKS.md` stays at the root.** It is written for a person setting the tool up, the
way the sibling's `MEMBER-GUIDE.md` is. The stage contracts route to its sections rather than
copy them.

**The chatbot prompt is kept, in `shared/`.** `new-chat-starter-prompt.md` is for someone
using an assistant that cannot read this folder. It duplicates what the stages say and
nothing regenerates it; `shared/CONTEXT.md` says so.

**Stage output is ignored by git.** A run is the creator's work, not the product. The
folders stay, held by `.gitkeep`, because a stage with no `output/` is not a stage.

**The root `output/` folder stays.** It holds the owner's scratch files and was already
ignored. The ignore rule became `/output/` so it no longer swallows the stages' own
`output/` folders.

**Approval is tied to a hash, not a path.** From the 2026-10-29 review: stage 04 records
the specification's SHA-256 and stage 05 compares it before exporting, with a one-line
standard-library command, so an edit after approval cannot be exported unnoticed.

**A revision archives what it supersedes.** Before stage 02 or 03 runs again for a study,
each later stage's files for it move to `output/archive/<date>/`. Continuation looks only
at `output/` itself, so a stale export cannot pass for progress, and nothing is deleted.

**No tool enforces the export gate.** The sibling's export command refuses an unapproved
check; here stage 05's contract makes the same demand of the assistant. The cold walk of
2026-11-01 showed the contract holds on its own, so enforcement is not planned.

## The Studio

**The study starter is a separate page beside the Studio, not a mode inside it.** Decided
2026-11-04. The owner wanted the tool easier to use: a page to fill in the blanks. A study
wants one page per passage with the same five sections every session, which the Studio's
blueprint does not lay out, and the Studio's editor draws and edits only lines, checklists and
choices, while a study page wants a callout and a split. So `studio/study-starter.html`
and `studio/study-starter.js` take the brand, the audience and one session per passage,
lay the pages out on the split recipe with row counts computed from the engine's own
height estimate, and use the Studio's server for checking, preview and the finished HTML.
The layout function is pure and `tests/test_study_starter.py` runs it under Node and hands
the result to the validator, so the starter cannot drift from what the engine accepts.
Teaching the Studio's editor the callout and split types, and then opening a starter study
in it, is the next step in `HANDOFF.md`; the starter was not made to wait for that.

**The design-system tokens are the authority for the Studio, and a test holds them.** Decided
2026-10-31, when `_config/design-system.md` and `studio/styles.css` were reconciled. Where
they disagreed, the document won for canvas (`#ececec`, which the palette specimen and the
page engine share) and the stylesheet won where its value was a deliberate accessibility or
density choice: Focus Blue `#275f7b` rather than Layout Slate for focus rings, because slate
does not reach contrast on white, and 8px × 13px button padding with a 40px minimum height.
Those became tokens. The page preview inside the editor copies the page engine's colours and
is not held to the tokens; `study_factory.py` owns those. `tests/test_design_tokens.py`
fails on any colour in the stylesheet that is neither a token nor an engine colour, and on
any token nothing in `studio/` uses.
