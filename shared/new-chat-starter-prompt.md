# New Chat Starter Prompt — Topical Study Studio

For a chatbot that cannot read this folder. An assistant that can should start at `CLAUDE.md` and walk `stages/` instead. Upload this folder, then paste the request below with your topic and desired page count.

---

Create a complete, printable planner set about: **[TOPIC]**.

Read `references/CONTENT_GUIDE.md`, then `references/DESIGN_STANDARD.md`, then inspect the approved reference HTML in `shared/examples/depression/approved-reference.html`. Treat the two references as requirements and the approved HTML as the look to match; its markup predates the current engine.

Before writing the JSON, make a private page blueprint. Give every page one sharply defined `concept`, one intended benefit, one mental task, one response form, and one composition. Remove semantic duplicates. Do not show me generic approval checkpoints; make sound decisions and complete the set.

Content requirements:

- Use supportive, specific, non-judgmental language. Never diagnose, prescribe, promise outcomes, force disclosure, or use toxic positivity.
- Keep each page focused on one concept and give it a small arc: arrive, notice, choose, act, close.
- Match response effort to the user’s likely capacity. Use bounded choices for low-energy moments and generous writing space for reflection.
- Where useful, translate intention into an if-then plan or one feasible next step.
- Do not repeat page concepts, prompts, section titles, interaction patterns, or adjacent layout silhouettes. Track wording across the whole set before finalizing.
- For health or mental-health topics, include appropriate scope/support language and flag the set for professional review before publication.

Design requirements:

- Exactly 816 x 1056 px per page, full safe-area use, precise aligned geometry, harmonious 14 px gutters, and no overlaps.
- Use the typography and palette in `references/DESIGN_STANDARD.md`; sentence-case section labels; no decorative clutter.
- Keep all content as text, borders and tables. Use supported content types before `custom_html`.
- Write a complete JSON spec from `shared/planner_spec_template.json`, run validation, generate HTML, and correct every error, collision, overflow, underfill, and repetition warning.
- Visually inspect every rendered page at full size and in print preview. Then print to PDF and verify page count, clipping, and complete corners.
- Provide the finished HTML and JSON and state exactly what remains to check before printing.

Set details:

- Page count: [COUNT]
- Audience/context: [AUDIENCE]
- Desired pages or outcomes: [LIST]
- Brand/footer: Simplify to Glorify | [TOPIC] Planner
