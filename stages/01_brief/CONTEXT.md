# 01_brief/CONTEXT.md: Layer 2 · Stage Contract

**One job:** write down what this study is, before any page is chosen.

Every later stage reads the brief, so a guess made here becomes a wrong study four stages
on. Ask; do not invent.

## Inputs

| Layer | What | Where | Section |
|---|---|---|---|
| 4 (working) | What the person wants: topic, who it is for, what it should help them do, how many pages | The person, in conversation, or a file they name | Full |
| 3 (reference) | The fields a brief has | `references/brief-template.md` | Full file |
| 3 (config) | What the product is and must not be | `../../_config/product.md` | Users, Product Purpose |
| 3 (reference) | The scope language a sensitive topic needs | `../../references/CONTENT_GUIDE.md` | Prompt design |

## Process

1. Choose a short name for the run in lower case with hyphens, such as `psalm-23`.
   It is the `<slug>` in every file name from here on.
2. Copy `references/brief-template.md` to `output/<slug>.brief.md` and fill in every field.
3. If the person has not said who the study is for, what it should help them do, or how
   many sessions and pages it has, ask. Leave a field marked `TO DECIDE` rather than fill it with a guess.
4. If the topic touches mental health, trauma, disability, medication, grief, addiction or
   crisis, mark **Sensitive topic: yes** so every later stage carries the scope language and
   the set is flagged for professional review.
5. Do not choose pages here. That is the next stage's job.

## Outputs

| Artifact | Location | Format |
|---|---|---|
| The brief | `output/<slug>.brief.md` | Markdown, the template filled in |

## Human gate

The person reads the brief and changes anything they like. Do not start stage 02 until they
say it is right and no field reads `TO DECIDE`.

## Next

`../02_pages/CONTEXT.md`
