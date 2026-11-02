# Topical Study Studio: How It Works

## Overview

Topical Study Studio is a small Python-based system for creating polished, printable pages from structured JSON files. It was built for planners and is being turned into a tool for topical Bible studies. The study pieces, Scripture blocks from the NASB 2020, a repeating session structure and a verse count, are not built yet, so this guide describes the tool as it works today.

You describe a planner set in JSON: its title, page concepts, section positions, prompts, writing areas, checklists, choices, and tables. The factory validates that description and converts it into a self-contained HTML document. Each generated page is exactly 816 × 1056 pixels, representing an 8.5 × 11-inch US Letter page.

The output uses ordinary HTML text, borders, lines, checkboxes, and tables instead of flattened images. This makes the pages suitable for browser review and crisp printing, and keeps them editable as HTML.

## What the factory does

The factory can:

- Generate one-page or multi-page planner sets
- Produce exact US Letter page dimensions
- Create writing lines, checklists, choices, callouts, tables, split sections, and custom HTML areas
- Apply consistent typography, colors, borders, margins, spacing, and footers
- Detect blocks outside the page or below the safe printing area
- Detect overlapping blocks
- Warn when a page does not use enough of the available sheet
- Detect repeated page concepts and repeated prompt wording
- Create a ready-to-edit starter specification for any topic
- Validate a specification without generating output

It does not produce the PDF itself. Printing to PDF and final visual verification remain separate human-reviewed steps.

## How it works

The workflow has five stages:

1. **Choose a topic and purpose.** Decide who the planner is for and what each page should help the user do.
2. **Create a JSON specification.** Define the planner set, pages, concepts, positioned blocks, and response formats.
3. **Validate the specification.** The factory checks geometry, page use, overlap, repeated concepts, and repeated wording.
4. **Generate HTML.** Valid JSON is rendered as one self-contained HTML document containing all planner pages.
5. **Review and print.** Open the HTML in a browser, inspect it at full and print size, correct any issues, and print it to PDF.

```text
Topic and audience
        ↓
JSON planner specification
        ↓
Layout and content validation
        ↓
Editable US Letter HTML pages
        ↓
Browser review → print to PDF → final verification
```

## What is needed

### Required

- Windows, macOS, or Linux
- Python 3.9 or newer
- The files in this repository
- A modern web browser such as Edge, Chrome, Firefox, or Safari
- A text editor for editing JSON

The generator uses only the Python standard library. No third-party Python packages are required.

### Optional

- Git, if you want to clone the repository or track your changes
- An AI assistant, if you want help planning page concepts or drafting a JSON specification

## Download or clone the project

Download the repository as a ZIP from GitHub and extract it, or clone it with Git:

```bash
git clone https://github.com/smiln32/topical-study-studio.git
cd topical-study-studio
```

The repository is public, so no GitHub sign-in is required to clone it.

## Confirm Python is available

Run one of these commands:

```bash
python --version
```

or:

```bash
python3 --version
```

The reported version should be 3.9 or newer. On systems where the command is `python3`, substitute `python3` for `python` in the examples below.

## Fastest first run

Create a starter specification for a topic:

```bash
python study_factory.py --init my-planner.json --topic "Morning Routine"
```

This creates `my-planner.json` with one complete example page. The topic is inserted into its title and footer.

Validate it:

```bash
python study_factory.py my-planner.json my-planner.html --validate-only
```

Generate the planner:

```bash
python study_factory.py my-planner.json my-planner.html
```

Open `my-planner.html` in a web browser. You should see a full US Letter planner page with four editable-content sections.

## Available commands

### Show the version

```bash
python study_factory.py --version
```

### Create a starter specification

```bash
python study_factory.py --init FILE.json --topic "TOPIC"
```

### Validate without generating

```bash
python study_factory.py SPEC.json OUTPUT.html --validate-only
```

The output filename is still supplied for command consistency, but no HTML file is written in validation-only mode.

### Generate planner HTML

```bash
python study_factory.py SPEC.json OUTPUT.html
```

## Understanding the JSON specification

A specification contains set-level information and an ordered list of pages:

```json
{
  "set_title": "Morning Routine Planner",
  "footer_label": "Simplify to Glorify | Morning Routine Planner",
  "pages": [
    {
      "concept": "Choose one realistic morning priority",
      "title": "My Morning Focus",
      "subtitle": "Begin with one useful next step.",
      "theme": "#b2c6b1",
      "blocks": []
    }
  ]
}
```

Each block has exact page coordinates and a content definition. For example:

```json
{
  "x": 28,
  "y": 104,
  "w": 760,
  "h": 260,
  "title": "What matters today",
  "color": "sage",
  "content": {
    "type": "lines",
    "prompt": "A few words are enough.",
    "rows": 7
  }
}
```

The complete field-by-field format is documented in [`references/SPECIFICATION.md`](references/SPECIFICATION.md).

## Supported response formats

- `lines` — open writing space
- `checklist` — labeled and blank checkbox rows
- `choices` — radio-style or checkbox-style options
- `callout` — short guidance with optional writing space
- `table` — repeated-row trackers and logs
- `split` — two related response areas
- `custom_html` — trusted custom markup for advanced cases

Prefer the standard types. They are easier to validate and keep visually consistent.

## Validation results

The factory returns one of three exit codes:

- `0` — the HTML was generated, or validation-only passed with no warnings
- `1` — validation-only finished with advisory warnings and no errors
- `2` — the specification could not be read, or validation found an error, in either mode

Only `--validate-only` reports warnings in the exit code. Plain generation writes the HTML and exits `0` even when warnings were printed, so read the terminal, not just the exit code, before treating a file as finished.

Typical findings include:

- A block extends outside the 816 × 1056 page
- A block enters the header or footer area
- Two blocks overlap
- The content stops too high and leaves an accidental empty lower section
- Two pages use the same concept
- A prompt or section title is repeated

Correct errors before generating or publishing. Review warnings rather than automatically ignoring them.

## Design and content guidance

Three documents guide planner quality:

- [`references/DESIGN_STANDARD.md`](references/DESIGN_STANDARD.md) defines the grid, spacing, typography, colors, safe areas, and visual checks.
- [`references/CONTENT_GUIDE.md`](references/CONTENT_GUIDE.md) explains how to write supportive, specific, non-repetitive prompts.
- [`references/SPECIFICATION.md`](references/SPECIFICATION.md) documents the JSON format and all supported content types.

Give every page one distinct concept. A page should help the user notice, choose, plan, track, reflect, or act on one focused idea. Avoid repeating the same prompt, response format, and layout silhouette throughout a set.

## Reviewing generated pages

Before importing or publishing:

1. Open the generated HTML in a modern browser.
2. Review every page at 100% zoom.
3. Check the browser's print preview at US Letter size.
4. Confirm headings and prompts are not clipped.
5. Confirm writing areas are large enough to use.
6. Confirm boxes do not overlap and their corners are complete.
7. Confirm content reaches the lower portion of the page without entering the footer.
8. Read every prompt for usefulness, tone, repetition, and safety.

A file that generates successfully is not automatically a finished planner. Visual and editorial review are required.

## Printing to PDF

After the browser review:

1. Open the generated HTML in the browser you will print from.
2. Print to PDF at US Letter, with no margins and background graphics turned on.
3. Confirm the expected page count.
4. Inspect every page of the PDF rather than relying on thumbnails.
5. Check that lines, boxes, checkboxes, and table borders printed completely.
6. Correct any font substitution, clipping, or alignment change in the specification, then regenerate and print again.
7. Keep the HTML and JSON beside the PDF so the set can be revised later.

Print output can differ between browsers, so the actual PDF must always be checked.

## Working with an AI assistant

The repository is laid out as an Interpretable Context Methodology (ICM) workspace. An assistant reads `CLAUDE.md` for the rules, `CONTEXT.md` for where a task goes, and then the `CONTEXT.md` inside each of the five stage folders under `stages/`: brief, pages, spec, check, export. Each stage writes plain files to its own `output/` folder and stops so you can read and edit them before the next stage begins. Nothing is exported until you tick **Approved for export** in the check report.

## Project structure

```text
CLAUDE.md                      Where an assistant is, and the rules
CONTEXT.md                     Where a task goes
stages/                        The planner build as five folders, one contract each
_config/                       What Topical Study Studio is and how it looks
references/                    SPECIFICATION.md, DESIGN_STANDARD.md, CONTENT_GUIDE.md
shared/                        Specification template, examples, chatbot prompt
records/                       The ICM structure audit
study_factory.py             Generator and validator
study_studio.py              Local server behind Topical Study Studio
studio/                        Topical Study Studio
tests/                         Automated unit tests
assets/                        Repository preview images and approved design references
HOW_IT_WORKS.md                This guide
DECISIONS.md                   Why things are the way they are
HANDOFF.md                     What comes next
RIGHTS_AND_ATTRIBUTION.md      Ownership of the original assets and third-party notices
LICENSE                        MIT
.github/workflows/             GitHub Actions validation
```

## Running the automated tests

From the repository root:

```bash
python -m unittest discover -s tests -v
```

The test suite checks example validation, exact page structure, overlap detection, duplicate concepts, invalid geometry, starter-file behavior, semantic version formatting, the Studio's assets and health endpoint, and the ICM structure: that every stage has its contract, that every path a contract names exists, and that the router names every stage.

GitHub Actions runs these checks automatically after every push to `main` and for pull requests. It also validates the basic and full depression specifications and exercises the CLI starter workflow.

## Troubleshooting

### `python` is not recognized

Install Python 3.9 or newer from the official Python website or your operating system's package manager. On macOS or Linux, try `python3`.

### JSON cannot be read

Check for missing commas, unmatched braces, invalid quotation marks, or non-JSON comments. Start from `shared/planner_spec_template.json` or generate a new starter file.

### Validation returns warnings

Read each warning in the terminal. A warning usually indicates an underfilled page or another layout concern that needs human review.

### Validation returns an error

Correct invalid coordinates, page bounds, overlaps, missing pages, repeated concepts, or other reported errors. Error exit code `2` means the specification should not be treated as ready.

### The printed PDF looks different

Check that the print dialog is set to US Letter with no margins and background graphics on. Compare the PDF with the browser-rendered HTML and adjust the specification as needed. A different browser may print more faithfully.

## Sensitive content

The factory can structure supportive reflection, but it is not a clinical tool and does not provide diagnosis, treatment, crisis care, or medical advice.

Planners and studies that touch mental health, trauma, disability, medication, grief, addiction, or crisis require careful human review by an appropriately qualified professional before publication. Never use a planner or a study as a substitute for emergency or professional support.

## What is changing

The next product is a topical Bible study: six or so sessions on one subject, each a few pages that take the reader through a passage and into application, printed as a PDF. Scripture will be quoted from the NASB 2020 under its publisher's quotation terms, the check stage will count the verses, and the export will print the copyright notice. The study content types, the session structure and the study content guide do not exist yet. [`README.md`](README.md) lists what is planned under "Where it is going", and [`HANDOFF.md`](HANDOFF.md) says what comes first.

## Summary

To use Topical Study Studio successfully, you need Python, a JSON specification, and a browser. The factory turns the JSON into precise US Letter HTML pages, validates common layout and repetition problems, and supports a human-reviewed path to a printed PDF. The design, content, and specification guides provide the standards needed to turn generated output into a polished set of pages.
