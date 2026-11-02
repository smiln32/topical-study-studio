# shared/CONTEXT.md: resources more than one stage uses

Layer 3. Nothing here changes from one planner run to the next.

| What | Where | Used by |
|---|---|---|
| A starter specification to copy | `planner_spec_template.json` | Stage 03, anyone writing a specification by hand |
| A two-page example and its output | `examples/basic/` | Tests, CI, anyone learning the format |
| A full planner, its generated output and the approved visual reference | `examples/depression/` | CI, stage 03 as a model of a finished set |
| An earlier planner as a PDF, for comparison only | `examples/adhd/planner-pages.pdf` | People; no stage reads it |
| One Bible study session built from the planner types; the source of the README image | `examples/study/` | People; no stage reads it |
| The whole build as one prompt for a chatbot without this folder | `new-chat-starter-prompt.md` | People using an assistant that cannot read the stages |

`examples/basic/output.html` must be exactly what the engine produces from
`examples/basic/spec.json`.
Regenerate it after any change to how a page prints.

`new-chat-starter-prompt.md` is derived from the stage contracts and the references. Nothing
regenerates it, so when a contract changes, read it again.
