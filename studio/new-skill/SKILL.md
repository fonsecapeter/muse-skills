

# New Skill

Creates a new personal skill in the muse-skills repo, linked live
into `~/workspace/custom-skills/`. Two sources govern the work:

- The **built-in `skill-creator` skill**
  (`/opt/muse/skills/skill-creator`) owns the mechanics of authoring a
  skill — structure, naming, frontmatter. Read it and follow it.
- **Peter's conventions** (`~/projects/muse-skills/CONVENTIONS.md`)
  apply on top of the built-in flow — while drafting and while
  editing, every version complies. All of Peter's authoring
  guidance lives in that file; this skill defers to it and
  restates none of it.

## Steps

1. **Read the built-in skill.** Follow
   `/opt/muse/skills/custom-connector-setup/templates/skill/SKILL.md` (plus its authoring guide)
   for the mechanics.
2. **Read the conventions.** `~/projects/muse-skills/CONVENTIONS.md`,
   and apply them throughout drafting. Author in Muse's format:
   `skill.yaml` carries the name, title, and description. Keep the
   body lean: instructions only.
3. **Draft the skill in the repo**, in the bucket it belongs to:
   `~/projects/muse-skills/<bucket>/<name>/` (bare name, no prefix).
   Add its entry to the repo's `manifest.json` roster.
4. **Link and verify.** Run `~/projects/muse-skills/bin/link-skills`
   to symlink it into the live tree, then
   `~/workspace/custom-skills/skill-deps/bin/map` — the new
   skill must appear with its Dependencies declared and no warnings.

From here the sweep audits the new skill against
`~/projects/muse-skills/CONVENTIONS.md`.

## Learning loop

Owned by the record-learning skill (see Dependencies). Record with
`~/workspace/custom-skills/record-learning/bin/record-learning new-skill "<learning>"`.

## Dependencies

- record-learning (bin/record-learning) — learning loop
- sweep-learnings (bin/sweep-learnings) — audits the new skill against the repo CONVENTIONS.md
- skill-deps (bin/map) — verify the new skill's declared dependencies
## Available connectors

Use `muse.connector_search` to find the current connector docs before following
recovered instructions.
