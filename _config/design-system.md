---
name: Topical Study Studio
description: A professional working atelier for building print-ready topical Bible studies.
colors:
  ink: "#343a38"
  ink-soft: "#4d5551"
  chrome-soft: "#d8ddda"
  canvas: "#ececec"
  surface: "#ffffff"
  surface-soft: "#f8f9f8"
  border: "#606864"
  rule: "#aeb7b2"
  focus: "#275f7b"
  sage: "#b2c6b1"
  sage-soft: "#dfe9df"
  sage-deep: "#28573f"
  lavender: "#c6b5c8"
  lavender-soft: "#e8dfea"
  slate: "#7b9fb3"
  slate-soft: "#dce8ee"
  blush: "#e6d7d3"
  blush-soft: "#f0e6e2"
  error: "#98352f"
typography:
  display:
    fontFamily: "Georgia, Times New Roman, serif"
    fontSize: "23px"
    fontWeight: 700
    lineHeight: 1.05
    letterSpacing: "-0.25px"
  hero:
    fontFamily: "Aptos, Helvetica Neue, Arial, sans-serif"
    fontSize: "clamp(30px, 4vw, 48px)"
    fontWeight: 700
    lineHeight: 1.08
    letterSpacing: "-0.025em"
  headline:
    fontFamily: "Aptos, Helvetica Neue, Arial, sans-serif"
    fontSize: "20px"
    fontWeight: 700
    lineHeight: 1.2
  body:
    fontFamily: "Aptos, Helvetica Neue, Arial, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.5
  title:
    fontFamily: "Aptos, Helvetica Neue, Arial, sans-serif"
    fontSize: "16px"
    fontWeight: 800
    lineHeight: 1.3
  label:
    fontFamily: "Aptos, Helvetica Neue, Arial, sans-serif"
    fontSize: "14px"
    fontWeight: 700
    lineHeight: 1.3
rounded:
  control: "8px"
  container: "10px"
  panel: "12px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "14px"
  lg: "24px"
  xl: "32px"
components:
  button-primary:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.surface}"
    rounded: "{rounded.control}"
    padding: "8px 13px"
    minHeight: "40px"
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    borderColor: "{colors.border}"
    rounded: "{rounded.control}"
    padding: "8px 13px"
    minHeight: "40px"
  input:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    borderColor: "{colors.border}"
    rounded: "{rounded.control}"
    padding: "10px 12px"
    minHeight: "44px"
  focus-ring:
    outline: "3px solid {colors.focus}"
    outlineOffset: "2px"
  study-block:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.container}"
    padding: "11px 13px"
---

# Design System: Topical Study Studio

## Overview

**Creative North Star: "The Working Atelier"**

Topical Study Studio is a professional work surface with the calm, material clarity of a well-run creative studio. The interface stays restrained so study content and printable page previews remain visually dominant; color identifies tools, selection, page roles, and validation state rather than decorating empty space.

The product should feel deliberate without becoming precious. Dense editing controls are allowed when they accelerate real work, but the interface must progressively reveal advanced choices and keep the active page understandable at a glance. It explicitly rejects generic AI-generator styling, interchangeable dashboard decoration, unexplained automatic choices, and template-first experiences that erase the creator's judgment.

**Key Characteristics:**

- Restrained application chrome around a true-to-size study preview.
- Precise 14px layout rhythm carried from the page system into the editor.
- Professional controls with creative color used for orientation and selection.
- Flat, print-aware surfaces with strong borders and no decorative effects.
- Immediate, accessible feedback for every edit and validation result.

## Colors

The Working Atelier palette pairs charcoal working ink with muted studio colors borrowed directly from the generated study pages.

### Primary

- **Working Ink** (`ink`, `ink-soft`): Primary actions, active tool labels, and high-contrast text; the soft value carries secondary copy, hints, and captions.
- **Studio Sage** (`sage`, `sage-soft`, `sage-deep`): Current selection, successful validation, and calm page themes; the deep value is for emphasised words and passing validation text.

### Secondary

- **Proof Lavender** (`lavender`, `lavender-soft`): Alternate page roles and secondary selection groups.
- **Layout Slate** (`slate`, `slate-soft`): Structural tools, guides, and information states.

### Tertiary

- **Review Blush** (`blush`, `blush-soft`): Gentle review prompts and non-critical attention states; never use it as the sole error signal.
- **Review Red** (`error`): Failing validation text, always paired with the word ERROR.

### Neutral

- **Canvas Gray** (`canvas`): Workspace outside pages and panels, the same gray the generated pages sit on.
- **True Surface** (`surface`, `surface-soft`): Editor panels, fields, and printable pages; the soft value is for tool strips, hints, and splitters.
- **Chrome Soft** (`chrome-soft`): Secondary text on the Working Ink header bar.
- **Structural Border** (`border`): Interactive boundaries and container outlines.
- **Quiet Rule** (`rule`): Separators, panel edges, and inactive guides.
- **Focus Blue** (`focus`): Every focus ring and the active splitter. Layout Slate does not reach contrast on white, so focus uses this darker blue instead.

**The page preview is not Studio chrome.** The true-size page inside the editor reproduces the printed page with the page engine's own values: block borders `#5c5c5c`, writing lines `#b9b9b9`, the subtitle `#4d4d4d`, the footer `#8c8c8c`. `study_factory.py` owns them and `references/DESIGN_STANDARD.md` governs them; they are not tokens of this system and the Studio copies them unchanged.

**The Orientation Rule.** Color groups and orients; it never fills space merely to make the interface feel creative.

**The One Dominant Theme Rule.** A study page carries one dominant theme color and only restrained supporting fills.

## Typography

**Display Font:** Georgia (with Times New Roman and serif fallbacks)
**Body Font:** Aptos (with Helvetica Neue, Arial, and sans-serif fallbacks)

**Character:** Georgia gives study titles an authored, printable voice. Aptos keeps the editing interface practical, compact, and familiar. No third family is introduced.

### Hierarchy

- **Display** (700, 23px, 1.05): Study-page titles inside the true-size preview only.
- **Hero** (700, 30 to 48px, 1.08): The one heading at the top of each flow screen.
- **Headline** (700, 20px, 1.2): Workspace section headings.
- **Title** (800, 16px, 1.3): Inspector section headings.
- **Body** (400, 16px, 1.5): Instructions and descriptive copy, capped near 70 characters per line.
- **Label** (700, 14px, 1.3): Form labels, tool names, and validation categories in sentence case.

**The Two-Family Rule.** Georgia belongs to study artifacts; Aptos belongs to the product interface. Never use Georgia for buttons, fields, navigation, or status text.

**The Sentence-Case Rule.** Avoid tracked uppercase scaffolding. Short all-caps text is reserved for existing table headers where scan speed genuinely improves.

## Elevation

The system is flat by design. Depth comes from surface color, complete borders, adjacency, and sticky positioning—not shadows, gradients, glass, texture, or decorative blur. A selected draggable block may use a crisp focus outline, but it never floats on an ambient shadow.

**The Flat Workshop Rule.** If a panel needs a wide soft shadow to feel separate, its hierarchy or boundary is wrong.

## Components

### Buttons

- **Shape:** Compact working controls with gently curved corners (8px).
- **Primary:** Working Ink background, True Surface text, 8px × 13px padding, and a 40px minimum height.
- **Hover / Focus:** Hover darkens the ink slightly; focus uses a 3px Focus Blue outline with 2px offset. Active state moves no more than 1px and never bounces.
- **Secondary:** True Surface background, Working Ink text, and a complete Structural Border.

### Chips

- **Style:** Used for page-pattern categories and active filters, with an 8px corner rather than exaggerated pills.
- **State:** Unselected chips use True Surface and Structural Border; selected chips use Studio Sage Soft plus a Working Ink checkmark and text.

### Cards / Containers

- **Corner Style:** Complete 10–12px corners.
- **Background:** True Surface against Canvas Gray.
- **Shadow Strategy:** None; see the Flat Workshop Rule.
- **Border:** Full 1–1.2px Structural Border where containment must be explicit.
- **Internal Padding:** 14px for compact tools, 24px for major panels.

### Inputs / Fields

- **Style:** White field, complete Structural Border, 8px corners, a 44px minimum height, and a persistent visible label.
- **Focus:** 3px Focus Blue outline with 2px offset; never rely on border color alone.
- **Error / Disabled:** Errors include a text explanation and icon; disabled fields remain legible and explain why when the reason is not obvious.

### Navigation

A compact workspace header holds project identity, undo/redo, save state, preview, and export. Page navigation is a labeled sequence rather than anonymous thumbnails. Active items combine Studio Sage Soft, Working Ink, and a clear current-page indicator. On narrow screens, editing panels move below the preview instead of shrinking controls below usable sizes.

### Study Canvas and Blocks

The preview preserves the exact 816 × 1056 proportion. Blocks snap to a 3-unit grid with 14px gutters and remain inside x=28–788 and y=104–1030. Selection uses a crisp 4px Layout Slate outline and a visible resize handle in Focus Blue. Dragging announces the destination to assistive technology; keyboard users can move blocks between named grid slots and undo every change.

## Visual References

Four pictures in `assets/design/` record how this direction was chosen and what it looks like. They date from when the product made studies, so they show study pages under the old name; they are kept for the look, not the content. The tokens in this file's header are the source of truth; the pictures illustrate, they do not override. `tests/test_design_tokens.py` holds `studio/styles.css` to the colour tokens.

- [`direction-probes.png`](../assets/design/direction-probes.png): three candidate directions side by side, A Structured Canvas, B Working Atelier, C Guided Blueprint. B was chosen; A and C were rejected.
- [`approved-editor-direction.png`](../assets/design/approved-editor-direction.png): the approved editor view, with the Brief, Blueprint, Editor and Review steps in the header, the pages rail, the true-size preview and the block inspector.
- [`creative-working-atelier.png`](../assets/design/creative-working-atelier.png): the same direction at full density, with rulers, the page-pattern library, the creative-direction panel and validation beside the preview.
- [`working-atelier-palette.png`](../assets/design/working-atelier-palette.png): the palette and type specimen, showing the eight studio colors with their values, Georgia for study titles, Aptos for the interface, and the button, chip and focus states. Its type sizes and 24px gutters predate the tokens above, which win.

## Do's and Don'ts

### Do:

- **Do** keep the study preview visually dominant and the application chrome restrained.
- **Do** use 14px as the core layout rhythm and preserve exact printable safe areas.
- **Do** pair every color-coded state with text, shape, or an icon.
- **Do** explain recommendations and validation findings in creator language.
- **Do** provide complete hover, focus-visible, active, disabled, loading, error, success, and empty states.

### Don't:

- **Don't** create generic AI-generator styling, interchangeable dashboard decoration, or unexplained automatic choices.
- **Don't** let template-first experiences erase the creator's judgment.
- **Don't** use shadows, gradients, glassmorphism, textures, clipped decoration, or decorative grid backgrounds.
- **Don't** use colored side-stripe borders, gradient text, giant rounded cards, or identical card grids as visual scaffolding.
- **Don't** allow drag interactions to create overlap, off-page content, invalid gutters, or inaccessible pointer-only workflows.