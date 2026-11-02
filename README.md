# Topical Study Studio

[![Validate Topical Study Studio](https://github.com/smiln32/topical-study-studio/actions/workflows/validate.yml/badge.svg)](https://github.com/smiln32/topical-study-studio/actions/workflows/validate.yml) [![Release](https://img.shields.io/badge/release-v1.1.0-6f8f72)](https://github.com/smiln32/topical-study-studio/releases/tag/v1.1.0) [![License: MIT](https://img.shields.io/badge/license-MIT-7b9fb3.svg)](LICENSE)

Topical Study Studio turns a JSON specification into printable US Letter pages. It renders print-ready HTML at exactly 816 × 1056 pixels, validates the layout and the wording, and a browser prints the result to PDF.

It was built for wellness planners and is being turned into a tool for **topical Bible studies**: a study is a set of sessions, each a few pages that take the reader through a passage and into application. The engine, the validator, Topical Study Studio and the five-stage build all carry over. The study-specific pieces, listed under [Where it is going](#where-it-is-going), do not exist yet, so the tool builds planners exactly as documented here until they do.

Each page is designed around one clear concept, with response formats and layouts chosen to match its purpose.

![A generated Bible study page: a session on Psalm 23 with a passage to copy out, observation lines, words to look up, interpretation lines and an application prayer](assets/study-preview.png)

## What it provides

- Exact 816 × 1056 px US Letter pages
- Editable HTML text, writing lines, checkboxes, tables, and section containers
- Consistent typography, spacing, margins, borders, and color roles
- Validation for page bounds, underfilled layouts, overlapping blocks, repeated concepts, and repeated prompts
- Content guidance for encouraging reflection without shame, pressure, forced positivity, or unnecessary repetition
- Reusable JSON specifications for producing complete planner sets
- Example specifications and approved visual references

## Where it is going

The next product is a topical Bible study: six or so sessions on one subject, printed as a PDF for individual or small-group use. What that needs, none of it built yet:

- **Scripture from the NASB 2020** (New American Standard Bible, The Lockman Foundation). Up to 500 verses may be quoted in one work under the publisher's gratis-use policy, and the copyright notice cites 2020 only. The check stage will count verses and the export will print the notice.
- **Study content types:** a passage with observation space, a cross-reference table, a memory-verse card, numbered discussion questions, and a prayer page.
- **A session structure that repeats by design**, so the validator's uniqueness rules apply within a session rather than across the whole set.
- **A content guide for studies:** observation, interpretation, application, in that order, with questions that send the reader back to the text.

## Requirements

- Python 3.9 or newer
- A modern web browser for reviewing generated HTML

No third-party Python packages are required.

## The Studio

The Studio is the visual, local-first way to create a complete planner without editing JSON coordinates. It guides you from a customer brief to a recommended page blueprint, then lets you edit, reorder, validate, and export the planner in your browser.

```bash
python study_studio.py
```

The studio opens at `http://127.0.0.1:8765`. Drafts are saved in that browser on your computer. Nothing is uploaded to a service or account. Use **Download editable project** to keep a portable JSON backup and **Download finished HTML** for the print-ready pages.

Studio features include blueprint recommendations, page sequencing, a full-page preview, adjustable side panels, snap-to-grid movement by pointer or keyboard, undo and redo, local draft saving, production notes, validation, and HTML/JSON export.

Create a topic-aware starter specification:

```bash
python study_factory.py --init my-planner.json --topic "Morning Routine"
```

Show the installed version:

```bash
python study_factory.py --version
```

## Complete guide

For a plain-language explanation of the system, requirements, setup, commands, validation, and printing to PDF, read [`HOW_IT_WORKS.md`](HOW_IT_WORKS.md). AI assistants start at [`CLAUDE.md`](CLAUDE.md) and [`CONTEXT.md`](CONTEXT.md): the repository is laid out as an Interpretable Context Methodology (ICM) workspace, and the planner build is five stage folders under [`stages/`](stages/).

## Quick start

1. Clone or download this repository.
2. Read [`references/CONTENT_GUIDE.md`](references/CONTENT_GUIDE.md) for prompt-writing and page-uniqueness guidance.
3. Read [`references/DESIGN_STANDARD.md`](references/DESIGN_STANDARD.md) for the required visual and layout system.
4. Copy [`shared/planner_spec_template.json`](shared/planner_spec_template.json) and replace the sample content with your planner topic and pages.
5. Give every page a distinct `concept` and define its content blocks.
6. Validate the specification, generate the HTML, and inspect every page before printing it.

Generate a planner:

```bash
python study_factory.py planner_spec.json output.html
```

Validate without creating an output file:

```bash
python study_factory.py planner_spec.json output.html --validate-only
```

Validation messages are written to the terminal. Errors must be corrected before publication; layout warnings should be reviewed rather than ignored.

## Specification overview

A planner specification contains set-level information and a list of pages. Each page includes a title, subtitle, theme color, unique concept, and positioned content blocks.

```json
{
  "set_title": "My Planner",
  "footer_label": "My Brand | My Planner",
  "pages": [
    {
      "concept": "Choose one realistic priority",
      "title": "A Gentle Priority",
      "subtitle": "Make today smaller and more workable.",
      "theme": "#b2c6b1",
      "blocks": []
    }
  ]
}
```

See [`shared/planner_spec_template.json`](shared/planner_spec_template.json) and the [`shared/examples/basic`](shared/examples/basic) directory for complete examples.

## Supported content types

- `lines` — open writing space
- `checklist` — predefined and blank checklist items
- `choices` — radio-style or checkbox-style choices
- `callout` — short guidance followed by optional writing lines
- `table` — structured trackers and logs
- `split` — two related response areas
- `custom_html` — an advanced escape hatch for layouts not covered by the standard types

Use `custom_html` sparingly. Standard content types are easier to validate and keep visually consistent.

## Design principles

Every page should:

- Focus on one useful concept
- Ask specific, answerable questions
- Match the response format to the mental effort required
- Provide practical writing space
- Avoid repeating wording or composition from nearby pages
- Move gently from noticing toward a choice, support, or feasible next step
- On a study page, send the reader to the passage before asking for a response
- Remain legible in print preview and on paper

The full JSON format is documented in [`references/SPECIFICATION.md`](references/SPECIFICATION.md). Visual requirements are documented in [`references/DESIGN_STANDARD.md`](references/DESIGN_STANDARD.md).

## Using the project with an AI assistant

An assistant that can read this folder starts at [`CLAUDE.md`](CLAUDE.md) and walks the five stages under [`stages/`](stages/), stopping for your approval after each. For a chatbot that cannot read the folder, [`shared/new-chat-starter-prompt.md`](shared/new-chat-starter-prompt.md) contains the same build as one reusable prompt. Provide the desired topic, audience, page count, and outcomes.

AI-generated planner content and layouts still require human review. Inspect wording, usefulness, visual balance, cultural fit, accessibility, and every rendered page before publishing or selling a set.

## Sensitive content

This project can help structure supportive reflection, but it is not a clinical tool and does not provide diagnosis, treatment, crisis care, or medical advice.

Planners and studies addressing mental health, trauma, disability, medication, grief, addiction, or other sensitive subjects should be reviewed by an appropriately qualified professional before publication. Crisis-related products should direct users to suitable local emergency or crisis resources and trusted human support.

## Printing to PDF

The generator creates ordinary HTML elements rather than flattened page images. After generation:

1. Review the HTML at full size and in the browser's print preview.
2. Correct clipping, overflow, cramped writing areas, or weak visual hierarchy.
3. Print to PDF at US Letter with no margins and background graphics turned on.
4. Confirm the page count and inspect every page of the PDF.
5. Keep the HTML and JSON beside the PDF so the set can be revised.

Print output differs between browsers, so always check the actual PDF before treating it as finished.

## Repository structure

```text
CLAUDE.md                      Layer 0: where an assistant is and the rules
CONTEXT.md                     Layer 1: where a task goes
stages/                        Layer 2: the planner build as five folders, each with a contract
  01_brief/ 02_pages/ 03_spec/ 04_check/ 05_export/
_config/                       Layer 3: product.md and design-system.md (Topical Study Studio)
references/                    Layer 3: SPECIFICATION.md, DESIGN_STANDARD.md, CONTENT_GUIDE.md
shared/                        Layer 3: planner_spec_template.json, examples/, the chatbot prompt
records/                       The ICM structure audit
study_factory.py             HTML generator and validator
study_studio.py              Local server behind Topical Study Studio
studio/                        Topical Study Studio
tests/                         Automated unit tests, including the structure test
assets/                        README preview images and approved design references
HOW_IT_WORKS.md                Plain-language setup and operating guide
DECISIONS.md                   Why things are the way they are
HANDOFF.md                     What comes next
RIGHTS_AND_ATTRIBUTION.md      Ownership of the original assets and third-party notices
LICENSE                        MIT
.github/workflows/             GitHub Actions validation
```

## Contributing

Contributions that improve validation, accessibility, print fidelity, documentation, content types, or layout precision are welcome. Keep changes consistent with the content and design standards and include a representative example when introducing a new content type.

## License

This project is available under the [MIT License](LICENSE). See [Rights and Attribution](RIGHTS_AND_ATTRIBUTION.md) for the scope of original project assets and third-party trademark notices.
