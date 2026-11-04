# shared/CONTEXT.md: resources more than one stage uses

Layer 3. Nothing here changes from one study run to the next.

| What | Where | Used by |
|---|---|---|
| A starter specification to copy | `study_spec_template.json` | Stage 03, anyone writing a specification by hand |
| One Bible study session and its output; the source of the README image | `examples/study/` | Tests, CI, anyone learning the format |
| The whole build as one prompt for a chatbot without this folder | `new-chat-starter-prompt.md` | People using an assistant that cannot read the stages |

`examples/study/output.html` must be exactly what the engine produces from
`examples/study/spec.json`, and a test holds it. Regenerate it after any change to how a page prints.

`new-chat-starter-prompt.md` is derived from the stage contracts and the references. Nothing
regenerates it, so when a contract changes, read it again.
