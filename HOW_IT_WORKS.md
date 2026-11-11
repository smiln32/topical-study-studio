# Topical Study Studio: How It Works

## Overview

Topical Study Studio is a small Python-based system for making topical Bible studies: six or so sessions on one subject, each a few pages that take the reader through a passage and into application, printed as a PDF.

You describe a study in a form or a JSON file: its title, sessions, passages, page concepts, prompts, writing areas, and tables. The tool validates that description and converts it into a self-contained HTML document. Each page is exactly 816 × 1056 pixels, representing an 8.5 × 11-inch US Letter page.

The output uses ordinary HTML text, borders, lines, checkboxes, and tables instead of flattened images. This makes the pages suitable for browser review and crisp printing, and keeps them editable as HTML.

## What the tool does

The tool can:

- Lay out a whole study from a fill-in-the-blanks form
- Print NASB 2020 passages with a reference line and verse numbers
- Produce exact US Letter page dimensions
- Create writing lines, checklists, choices, callouts, tables, split sections, and custom HTML areas
- Apply consistent typography, colors, borders, margins, spacing, and footers
- Detect blocks outside the page or below the safe printing area
- Detect overlapping blocks
- Warn when a page does not use enough of the available sheet
- Detect repeated page concepts and repeated prompt wording
- Refuse more than 500 quoted verses in one study
- Validate a specification without generating output

It does not produce the PDF itself. Printing to PDF and final visual verification remain separate human-reviewed steps.

## How it works

The workflow has five stages:

1. **Choose a topic and purpose.** Decide who the study is for, how many sessions it has, and what it should help them do.
2. **Choose the passages and pages.** Give each page one job, moving from what the text says to what it asks.
3. **Write the specification.** The study starter or the Studio writes it for you, or you write the JSON by hand.
4. **Validate and review.** The tool checks geometry, page use, overlap, repeated wording and the verse limit, and a person checks the rest.
5. **Print.** Open the HTML in a browser, inspect it at full and print size, and print it to PDF.

```text
Topic, audience and passages
        ↓
Study specification
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

## Fastest first study

Start the Studio and open the study starter:

```bash
python study_studio.py
```

Then go to `http://127.0.0.1:8765/study-starter.html`, or follow the link on the Studio's brief page. The starter is a form:

1. Name the study and the brand that prints in every footer, and choose a page colour.
2. Add one session per passage. Type the reference (for example `Psalm 23:1-3`) and a session title. The read, observe, interpret, apply and prayer prompts fill themselves with wording that names the passage; edit any of them. Add words to look up, up to ten, and up to four discussion questions if the session needs a second page.
3. Press **Check the study**. The same validator that checks the command line reports what it finds.
4. Press **Preview the pages** to see every page at true size, then **Download finished HTML** and print it as described under Printing to PDF, or **Download the specification (JSON)** to edit by hand or keep beside the PDF.

Each session becomes one page on the split layout: read the passage, observe beside words to look up, interpret, and apply beside a prayer. Row counts come from the engine's own height estimate, so the validator reports nothing, and every page reaches the bottom of the content area. What you type is saved in your browser, so the form survives a refresh; **Start over** clears it.

To quote the passage, paste its NASB 2020 text into the session, one verse per line, each starting with its number, and copy the publisher's notice from lockman.org into the study's notice field. The block grows to fit the text, and the rows below it give up the height; a passage too long for that gets pages of its own before the session page, and no verse or word to look up is ever dropped. The starter will not download HTML when the check says some text will not print. Without passage text the page tells the reader where to read and quotes nothing.

## Starting from the command line

Create a starter specification for a topic, validate it and generate it:

```bash
python study_factory.py --init my-study.json --topic "Psalm 23"
python study_factory.py my-study.json my-study.html --validate-only
python study_factory.py my-study.json my-study.html
```

Open `my-study.html` in a web browser. You should see one full US Letter session page.

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

### Generate study HTML

```bash
python study_factory.py SPEC.json OUTPUT.html
```

## Understanding the JSON specification

A specification contains set-level information and an ordered list of pages:

```json
{
  "set_title": "Psalm 23: Trusting the Shepherd",
  "footer_label": "Simplify to Glorify | Trusting the Shepherd",
  "pages": [
    {
      "concept": "See what the shepherd does in the psalm",
      "title": "Session 1: The Shepherd",
      "subtitle": "Psalm 23:1-3. Read the whole psalm before you begin.",
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
  "title": "Observe",
  "color": "sage",
  "content": {
    "type": "lines",
    "prompt": "What does the text say the shepherd does?",
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
- `passage` — quoted NASB 2020 Scripture with verse numbers
- `table` — structured rows such as a cross-reference table
- `split` — two related response areas
- `custom_html` — trusted custom markup for advanced cases

Prefer the standard types. They are easier to validate and keep visually consistent.

## Validation results

The generator returns one of three exit codes:

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

Three documents guide study quality:

- [`references/DESIGN_STANDARD.md`](references/DESIGN_STANDARD.md) defines the grid, spacing, typography, colors, safe areas, and visual checks.
- [`references/CONTENT_GUIDE.md`](references/CONTENT_GUIDE.md) explains how to write specific, text-driven, non-repetitive questions.
- [`references/SPECIFICATION.md`](references/SPECIFICATION.md) documents the JSON format and all supported content types.

Give every page one distinct concept. Send the reader to the passage first, and keep each session in order: observation, interpretation, application. Avoid repeating the same prompt, response format, and layout silhouette throughout a set.

## Reviewing generated pages

Before publishing:

1. Open the generated HTML in a modern browser.
2. Review every page at 100% zoom.
3. Check the browser's print preview at US Letter size.
4. Confirm headings and prompts are not clipped.
5. Confirm writing areas are large enough to use.
6. Confirm boxes do not overlap and their corners are complete.
7. Confirm content reaches the lower portion of the page without entering the footer.
8. Read every prompt for usefulness, tone and repetition, and check every reference and quotation.

A file that generates successfully is not automatically a finished study. Visual and editorial review are required.

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
stages/                        The study build as five folders, one contract each
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

GitHub Actions runs these checks automatically after every push to `main` and for pull requests. It also validates the example study and the template and exercises the CLI starter workflow.

## Troubleshooting

### `python` is not recognized

Install Python 3.9 or newer from the official Python website or your operating system's package manager. On macOS or Linux, try `python3`.

### JSON cannot be read

Check for missing commas, unmatched braces, invalid quotation marks, or non-JSON comments. Start from `shared/study_spec_template.json` or generate a new starter file.

### Validation returns warnings

Read each warning in the terminal. A warning usually indicates an underfilled page or another layout concern that needs human review.

### Validation returns an error

Correct invalid coordinates, page bounds, overlaps, missing pages, repeated concepts, or other reported errors. Error exit code `2` means the specification should not be treated as ready.

### The printed PDF looks different

Check that the print dialog is set to US Letter with no margins and background graphics on. Compare the PDF with the browser-rendered HTML and adjust the specification as needed. A different browser may print more faithfully.

## Sensitive content

This tool is not a clinical tool and does not provide diagnosis, treatment, crisis care, or medical advice.

Studies that touch mental health, trauma, disability, medication, grief, addiction, or crisis require careful human review by an appropriately qualified professional before publication. Never use a study as a substitute for emergency or professional support.

## What comes next

A study quotes Scripture from the NASB 2020 under its publisher's terms. The check stage will report the verses quoted and export will print the notice. More study content types and a repeating session structure are also still to come. [`HANDOFF.md`](HANDOFF.md) says what comes first.

## Summary

To use Topical Study Studio successfully, you need Python and a browser. The tool turns your description into precise US Letter HTML pages, validates common layout and repetition problems, and supports a human-reviewed path to a printed PDF. The design, content, and specification guides provide the standards needed to turn generated output into a polished set of pages.
