

# Skill Learning Sweep

This skill is the **single source of truth** for how custom skills learn.
Every custom skill's "Learning loop" section defers here. Three parts:

- **Record** (any time a learning surfaces, in any session):
  `bin/record-learning <skill-name> "<learning>"`
  Appends a dated entry to that skill's `learnings.md`.
- **Sweep** (nightly, or on demand): implement the pending learnings into
  the skills, then move each implemented learning into the central
  `learned.md` log with the skill id, the learning, and the change made:
  `bin/sweep-learnings --learned <skill> "<learning>" "<change>"`
  (`bin/sweep-learnings` lists pending; `--clear <skill>` empties a
  skill's log; `--recent [N]` shows recent learned entries).
- **Learned log** (`learned.md`, central): the permanent history of what
  was learned and what changed in response. The sweep also reads recent
  entries back open-endedly to spot broader patterns across skills.

## Recording learnings

- Record at the moment the learning is fresh: what worked, what Peter
  corrected, a tool/site quirk, a workflow fix. One learning per call,
  one or two lines, the durable rule — not the session story.
- **A correction from Peter is an automatic trigger.** Any time Peter
  corrects Tony's work, record the learning in that same turn,
  unprompted — do not wait for him to ask for it to be saved. Evidence:
  2026-10-13 Peter had to explicitly ask Tony to save the learning
  about the Notion checklist miss, though it was obvious the moment
  he corrected it.
- Each entry must stand on its own: state the rule AND one line of
  evidence (the incident, correction, or date) so the nightly sweep can
  implement it cold, without the session that produced it. A bare
  conclusion ("watch whether X") is not implementable — write what to
  do differently instead.
- The target is the skill it belongs to. Sweep-process learnings (e.g.
  "the log format drops X, store Y instead") target this skill,
  `learning-loop` — so one night's problems get solved by the
  next night's sweep.

## The sweep

1. Run `bin/sweep-learnings` to collect pending entries across the
   live tree (includes this skill's own log — the sweep sweeps
   itself). The live tree's symlinks resolve into the muse-skills
   repo, so implementing a learning edits the repo working tree;
   committing it is a separate, deliberate step.
2. For each learning, implement it in its skill per the workspace
   conventions (AGENTS.md): playbook in `SKILL.md`, machine values in
   `config.md`, deterministic work in a `bin/` CLI. Small durable edits;
   only what the evidence supports.
3. **Move implemented learnings to the learned log.** For every learning
   actually implemented, append it to the central log before removing it
   from the pending log:
   `bin/sweep-learnings --learned <skill> "<the learning>" "<the change made in response>"`
   Each entry records the date, the skill id, the learning as it was
   surfaced, and the concrete change made. Then clear the pending entries:
   `bin/sweep-learnings --clear <skill>` if all of a skill's entries were
   implemented, otherwise edit that `learnings.md` and delete just the
   implemented lines. Never remove an entry that hasn't actually been
   implemented — and never write a learned entry for one either.
4. **Audit best-practice compliance.** Independently of logged
   learnings, check every custom skill against `CONVENTIONS.md` in this
   directory: a "Learning loop" section deferring here, a "Dependencies"
   section with all cross-skill calls declared, deterministic work
   scripted as `bin/` CLIs wherever possible (not buried in prose),
   machine values in `config.md` rather than hardcoded in code, and any
   cron a one-liner pointing at its skill. Also verify mechanically: every
   skill has a `## Dependencies` section and `skill-deps/bin/map` reports
   no warnings (all declared deps resolve, no undeclared cross-refs).
   Fix mechanical drift directly; record anything bigger as a learning
   for that skill.
   **Duplicate CLI copies (learned 2026-10-14):** diff any `bin/` CLI
   that exists in more than one place across `~/workspace/custom-skills/` and
   `~/workspace/custom-connectors/` (e.g. notion's `bin/notion-api`
   also lives in `custom.legacy-notion/bin/`). Same-named files that
   are genuinely different CLIs for different skills (e.g. the two
   `scan-inbox` scripts) are not copies — skip them. For a true copy,
   a fix to one copy is incomplete until all copies match, or the
   extra copies are replaced by a deferral to the canonical one.
   Report any diff found, even when the copies currently match.
   (The learning-loop mirror in the old `~/workspace/skills/` tree
   was retired in the 2026-11-05 consolidation — there is one tree
   and one copy of everything now; nothing to diff against.)

## Operating rules

- Custom skills only (`~/workspace/custom-skills/`) — never edit bundled skills
  under `/opt/muse/skills/`.
- Storage: pending learnings stay per-skill — each skill's `learnings.md`
  holds its own, self-contained next to the skill they belong to
  (decision 2026-10-02: per-skill keeps skills composable and portable).
  Implemented learnings move to the **central** `learned.md` in this
  skill's directory, one entry per learning with the skill id, the
  learning, and the change made in response (decision 2026-10-06, Peter's
  call: central history makes cross-skill patterns visible). `learned.md`
  is append-only — entries are never edited or deleted.
  `bin/sweep-learnings` is the centralized view across all pending logs.
- The sweep touches only skill files (including `learnings.md`). Peter's
  external systems stay read-only.
- Latest dated evidence wins on conflict; genuinely unclear → hold and
  flag (step 6).

## Dependencies
- (none — this skill is the root of the learning loop; it sweeps its own log)

## Learning loop

This skill follows its own protocol: record sweep learnings with
`bin/record-learning learning-loop "<learning>"`; the nightly
sweep implements them, logs them in `learned.md`, and clears the pending
entries like any other skill's.
## Available connectors

Use `muse.connector_search` to find the current connector docs before following
recovered instructions.
