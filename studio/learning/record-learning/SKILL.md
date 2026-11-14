# Record Learning

Records a learning for a custom skill the moment it surfaces, so
the sweep (the sweep-learnings skill) can implement it later. One
learning per call:

`bin/record-learning <skill-name> '<learning>'`

Appends a dated entry to the central learning log, tagged with
the skill it belongs to. Learnings that span skills, or belong to
no single skill, are tagged `cross-skill` instead — same command,
target `cross-skill`.

**Quote with single quotes.** A learning containing a `$` amount
recorded inside double quotes loses the figure to shell expansion
(`$250` becomes `50`) — the 2026-11-12 simi-claims entry had to be
reconstructed from the declarations packet for exactly this reason.
Single quotes keep every character literal.

## What to record

- Record at the moment the learning is fresh: what worked, what
  Peter corrected, a tool/site quirk, a workflow fix. One or two
  lines: the durable rule, not the session story.
- **A correction from Peter is an automatic trigger.** Record it in
  the same turn, unprompted — do not wait for him to ask for it to
  be saved. Evidence: 2026-10-13 Peter had to explicitly ask Tony
  to save the learning about the Notion checklist miss, though it
  was obvious the moment he corrected it.
- Each entry must stand on its own: state the rule AND one line of
  evidence (the incident, correction, or date) so the sweep
  can implement it cold, without the session that produced it. A
  bare conclusion ("watch whether X") is not implementable — write
  what to do differently instead.
- The target is the skill it belongs to. Learnings about the
  learning process itself target the skill they belong to:
  record-learning or sweep-learnings.

## Storage

- One central log for everything pending:
  `<log_dir>/learnings.md` (`log_dir` in `config.md`), outside
  source control. Every entry is one line tagged with its skill —
  no per-skill queue files to keep in sync, and parallel sessions
  just append lines.
- The log only holds what's still pending. Whoever implements an
  entry — the sweep, or any session editing that skill —
  removes its line. There is no separate learned log: what changed
  in response is recorded by the repo itself, in the diff and its
  description.
- Any session about to edit a skill checks the log for entries
  tagged with that skill first.

## Learning loop

This skill is the recording half of the learning loop; the
sweep-learnings skill implements what it records. Record this
skill's own learnings with
`~/workspace/custom-skills/record-learning/bin/record-learning record-learning "<learning>"`.

## Dependencies

- (none — this skill's CLI is the one other skills call)
