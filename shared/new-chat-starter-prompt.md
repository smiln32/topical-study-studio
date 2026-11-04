# New Chat Starter Prompt — Topical Study Studio

For a chatbot that cannot read this folder. An assistant that can should start at `CLAUDE.md` and walk `stages/` instead. Upload this folder, then paste the request below with your topic and session count.

---

Create a complete, printable topical Bible study about: **[TOPIC]**.

Read `references/CONTENT_GUIDE.md`, then `references/DESIGN_STANDARD.md`, then inspect the example in `shared/examples/study/`. Treat the two references as requirements and the example as the look to match.

Before writing the JSON, make a private page blueprint. Choose the passages, then give every page one sharply defined `concept`, one thinking task, one response form, and one composition. Remove semantic duplicates. Do not show me generic approval checkpoints; make sound decisions and complete the set.

Content requirements:

- Take the reader to the passage before any question, then move through observation, interpretation and application, in that order.
- Ask specific questions the text can answer. Name the passage or verse each one depends on.
- Make application small and concrete, and close each session with a response, a prayer, or a next step.
- Quote Scripture only from the NASB 2020 and only from text I give you. Never quote from memory; where you have no text, tell the reader where to read. Keep the study under 500 quoted verses, and leave the copyright notice for me to copy from lockman.org.
- Do not repeat page concepts, prompts, section titles, interaction patterns, or adjacent layout silhouettes. Track wording across the whole set before finalizing.
- For a study on mental health, trauma, disability, medication, grief, addiction or crisis, include appropriate scope and support language and flag it for professional review before publication.

Design requirements:

- Exactly 816 x 1056 px per page, full safe-area use, precise aligned geometry, 14 px gutters, and no overlaps.
- Use the typography and palette in `references/DESIGN_STANDARD.md`; sentence-case section labels; no decorative clutter.
- Keep all content as text, borders and tables. Use supported content types before `custom_html`.
- Write a complete JSON spec from `shared/study_spec_template.json`, run validation, generate HTML, and correct every error, collision, overflow, underfill, and repetition warning.
- Visually inspect every rendered page at full size and in print preview. Then print to PDF and verify page count, clipping, and complete corners.
- Provide the finished HTML and JSON and state exactly what remains to check before printing.

Study details:

- Sessions and pages per session: [COUNT]
- Audience and setting: [AUDIENCE, ALONE OR LED CLASS]
- Passages, if chosen, and desired outcomes: [LIST]
- Brand/footer: Simplify to Glorify | [TOPIC] Study
