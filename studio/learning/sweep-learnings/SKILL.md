# Sweep Learnings

The nightly sweep: implements pending skill learnings, audits the
skills against `CONVENTIONS.md` (in this directory), and works the
central learning log. Learnings are recorded by the record-learning
skill; this skill consumes them.

`bin/sweep-learnings` lists the pending entries in the central
learning log. `--drop <skill>` removes a skill's entries once they
are implemented, printing what it removed.

## The sweep

1. **Collect pending.** Run `bin/sweep-learnings` — the whole
   central log in one list, this skill's own entries included (the
   sweep sweeps itself). One list means cross-skill patterns are
   visible directly, no separate review pass needed.
2. **Branch the repo.** In `~/projects/muse-skills`, branch off
   `main`, named for the work (`nightly-learnings`). If a learnings
   PR from a previous night is still open, add tonight's commit to
   its branch instead of opening a second PR.
3. **Implement each learning** in its skill, per `CONVENTIONS.md`:
   playbook in `SKILL.md`, machine values in `config.md`,
   deterministic work in a `bin/` CLI. Small durable edits; only
   what the evidence supports. Any code written follows the coding
   skill. Skills not yet in the repo (live-only directories) are
   implemented in place — their changes can't ride the PR yet; note
   them in the report.
4. **Drop implemented entries.** Once a skill's learnings are
   implemented, remove them from the log:
   `bin/sweep-learnings --drop <skill>` (on a partial implementation,
   edit the log and remove just those lines). Never drop an entry
   that hasn't been implemented. The PR in step 5 lists what was
   implemented — that listing, plus the diff itself, is the record
   of what changed; no separate learned log is kept.
5. **Open the diff.** Commit the repo changes (one commit), push,
   open a PR named for the work, its body listing the learnings
   implemented. Then schedule the morning note: a one-time cron for
   about 08:05 the next morning telling Peter a learning diff is
   waiting, with the PR link. If Peter calls the diffs noise, the
   fallback is committing straight to `main` — his call, recorded
   here when it changes.
6. **Audit compliance.** Independently of logged learnings, check
   every custom skill against `CONVENTIONS.md`: a "Learning loop"
   section deferring to record-learning, a "Dependencies" section
   with all cross-skill calls declared, deterministic work scripted
   as `bin/` CLIs wherever possible, machine values in `config.md`,
   any cron a one-liner pointing at its skill. Verify mechanically:
   `skill-deps/bin/map` reports no warnings. Fix mechanical drift
   directly (it rides the same diff); record anything bigger as a
   learning for that skill.
   **Duplicate CLI copies:** diff any `bin/` CLI that exists in
   more than one place across `~/workspace/custom-skills/` and
   `~/workspace/custom-connectors/`. Same-named files that are
   genuinely different CLIs for different skills are not copies —
   skip them. For a true copy, a fix to one copy is incomplete
   until all copies match, or the extra copies are replaced by a
   deferral to the canonical one. Report any diff found, even when
   the copies currently match.

## Operating rules

- Custom skills only (`~/workspace/custom-skills/`) — never edit
  bundled skills under `/opt/muse/skills/`.
- The sweep touches only skill files and the learning logs.
  Peter's external systems stay read-only.
- Storage: pending learnings live in the one central log
  (`<log_dir>/learnings.md`, outside source control), each tagged
  with its skill; implemented entries are removed from it. No
  learned log is kept — the repo's diffs are the history.
- Latest dated evidence wins on conflict; genuinely unclear → hold
  and flag in the report.

## Learning loop

This skill follows the protocol it runs: record its own learnings
with
`~/workspace/custom-skills/record-learning/bin/record-learning sweep-learnings "<learning>"`;
the next sweep implements them like any other skill's.

## Dependencies

- record-learning (bin/record-learning) — record audit findings as new learnings
- coding (SKILL.md) — any code written while implementing follows Peter's coding philosophy
