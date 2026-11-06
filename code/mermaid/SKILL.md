

# Mermaid

## Purpose

Turn a mermaid diagram definition into a rendered in-chat widget. The
agent writes the diagram; `bin/render` (deterministic) wraps it in the
widget HTML shell; the agent presents it with `widget.create`.

## Workflow

1. Write the mermaid definition. Keep node ids simple (`[a-z0-9_]`),
   put display labels in `["..."]`, use `<br/>` to wrap long labels,
   prefer `flowchart TD` / `flowchart LR`.
2. Run `bin/render` in this skill's directory:
   - `bin/render diagram.mmd --out /tmp/graph.html`, or
   - `some-cli | bin/render --out /tmp/graph.html` (reads stdin)
   
   Without `--out` it writes to `/tmp/mermaid-<epoch>.html`. It prints
   the output path.
3. Create the widget: `widget.create` with kind `html_file` and that
   path; embed the returned token in your reply.

## Output Contract

- `bin/render` prints the HTML file path and nothing else.
- The HTML is a compact fragment: mermaid.js loads from the CDN pinned
  in `config.md`, renders the definition to SVG on load.
- The widget stores the HTML whole at creation — the source file isn't
  needed afterwards, so `/tmp` output is fine.

## Operating Rules

- `theme: base` with comfortable node/rank spacing (set in `bin/render`,
  not per diagram).
- Style semantic classes with `classDef` (e.g. dashed for externals),
  not per-node inline styles.

## Learning loop

Owned by the learning-loop skill (see Dependencies). Record with
`~/workspace/custom-skills/learning-loop/bin/record-learning mermaid "<learning>"`.

## Dependencies

- learning-loop (bin/record-learning) — learning loop
## Available connectors

Use `muse.connector_search` to find the current connector docs before following
recovered instructions.
