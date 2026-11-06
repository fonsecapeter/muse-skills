

# Skill Deps

Deterministic dependency map for the personal (custom) skills in
`~/workspace/custom-skills/` (the live tree; per `config.md`
`skills_dirs`; the canonical name is the directory name — a legacy
`local-`/`local_` prefix, still on not-yet-migrated skills, is
stripped).
Built-in skills under `/opt/muse/skills/` are out of
scope — they show up only as `external` leaf nodes.

## Usage

Run `bin/map` in this skill's directory:

- `bin/map` — tree + mermaid + warnings
- `bin/map --tree` — indented tree only (token-cheap)
- `bin/map --mermaid` — mermaid graph only (for rendering)
- `bin/map --render [--out file.html]` — pipe the mermaid output through
  the mermaid skill's `bin/render`; prints the HTML path, ready for
  `widget.create` (kind `html_file`)

Exit 0 always; problems are reported as warnings, not failures.

## The Dependencies convention

Every personal skill declares its dependencies in a `## Dependencies` section
in its SKILL.md, one line per dependency, in this exact format:

```
- <skill-name> (<cli-path>) — <why>
```

- `<skill-name>` is the skill's canonical name: the directory name
  under `~/workspace/custom-skills/` (any legacy `local-` prefix
  stripped) — or an external name like `google_calendar`.
- `<cli-path>` is like `bin/notion-api`, or starts with `external` for
  things outside the personal skills dir (a built-in skill, a wallet
  provider, the live browser).
- A skill with no dependencies writes `- (none — <why>)`.

Example:

```
## Dependencies
- notion (bin/notion-api) — reads the TODO database; never reimplement auth
- record-learning (bin/record-learning) — learning loop
```

New skills: the new-skill skill requires this section — it wraps the
built-in skill-creator and applies Peter's conventions on top. If a skill
calls another skill's CLI, it must be declared here.

## Learning loop

Owned by the record-learning skill (see Dependencies). Record with
`~/workspace/custom-skills/record-learning/bin/record-learning skill-deps "<learning>"`.

## Dependencies

- mermaid (bin/render) — render the map's mermaid output as a widget (--render)
- record-learning (bin/record-learning) — learning loop
## Available connectors

Use `muse.connector_search` to find the current connector docs before following
recovered instructions.
