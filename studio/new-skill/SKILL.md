

# New Skill

Creates a new personal skill in the muse-skills repo, linked live
into `~/workspace/custom-skills/`. This skill is a
thin wrapper, not a replacement:

- The **built-in `skill-creator` skill**
  (`/opt/muse/skills/skill-creator`) owns the mechanics of authoring a
  skill — structure, naming, frontmatter. Read it and follow it.
- **Peter's conventions**
  (`~/workspace/custom-skills/learning-loop/CONVENTIONS.md`) apply **on
  top of** the built-in flow and must still be followed — while drafting
  and while editing, every version complies.

## Steps

1. **Read the built-in skill.** Follow
   `/opt/muse/skills/custom-connector-setup/templates/skill/SKILL.md` (plus its authoring guide)
   for the mechanics.
2. **Read the conventions.**
   `~/workspace/custom-skills/learning-loop/CONVENTIONS.md`: playbook in
   SKILL.md, machine values in `config.md`, deterministic work scripted
   as `bin/` CLIs wherever possible, crons as one-liners, declared
   Dependencies, learning-loop deferral. Apply throughout drafting — not
   as a cleanup pass at the end.
3. **Draft the skill in the repo**, in the bucket it belongs to:
   `~/projects/muse-skills/<bucket>/<name>/` (bare name, no prefix).
   Add its entry to the repo's `manifest.json` roster.
4. **Link and verify.** Run `~/projects/muse-skills/bin/link-skills`
   to symlink it into the live tree, then
   `~/workspace/custom-skills/skill-deps/bin/map` — the new
   skill must appear with its Dependencies declared and no warnings.

From here the nightly sweep audits the new skill against CONVENTIONS.md.

## Learning loop

Owned by the learning-loop skill (see Dependencies). Record with
`~/workspace/custom-skills/learning-loop/bin/record-learning new-skill "<learning>"`.

## Dependencies

- learning-loop (bin/record-learning) — learning loop; CONVENTIONS.md lives here
- skill-deps (bin/map) — verify the new skill's declared dependencies
## Available connectors

Use `muse.connector_search` to find the current connector docs before following
recovered instructions.
