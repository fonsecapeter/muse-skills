---
name: "todo-update"
description: "Update an existing TODO"
---

# Todo Update

Updating existing todos in Peter's TODO database: closing, parking,
adding info. The notion skill owns the API mechanics; all Notion
access defers to its `bin/notion-api`.

System map: `~/workspace/custom-skills/SYSTEM.md` — how Peter's
capture → todos → digests → completions system fits together, and
the cross-cutting rules (status meanings, read-only by default).

## The completion signal (standing authorization)

When Peter reports in chat that something is done — "I did it", "done",
"updated Xfinity", "booked it" — that report IS the authorization to
update the matching todo. No separate ask needed. Then:

1. **Find the todo** with todo-find's `bin/find-todo` (try several
   title phrasings). If nothing matches, say so and ask where it
   belongs — don't log the completion somewhere else instead
   (goal timeline, daily log, and memory don't count as updating
   the todo).
2. **Whole task done** → set Status to Done.
3. **Partial completion** — one item of a bigger, still-open todo (one
   merchant in a migration checklist, one step of an umbrella) → keep
   the todo open and check the item in the todo's own body checklist
   with `bin/check-item`. An appended progress paragraph is not a
   substitute for checking the box.
4. **Verify** the new state (both CLIs re-read after writing) before
   reporting back.
5. **Jeep project?** If the todo belongs to the Jeep project and the
   completion is work performed on the Jeep, it isn't finished until
   the work is also logged in the Jeep Service Log. That logging is
   owned by the jeep-log skill; follow it — don't duplicate the
   logging logic here. Jeep project only.

History: this rule lives here, in the skill named for the task,
because as fine print in the notion skill it missed twice
(2026-10-06 checkbook, 2026-10-13 Xfinity partial completion).

## Other updates (Peter's explicit ask)

- **Park / revive:** set Status to Parked, or back to TODO when he
  revives it.
- **Due dates:** set or move one only when he names it — a due date
  is a real commitment, never a loose plan (the rule as todo-file
  states it for new todos).
- **Adding info:** append to the body or add checklist items,
  following todo-file's body-writing rules. Nothing gets checked off
  except through the completion signal or Peter's own spot-test.

## Tooling

- `bin/check-item <page-id> "<item text>" [--off]` — checks (or
  unchecks) the one matching `to_do` block in a todo's body, then
  re-reads to verify. Fails loudly on zero or multiple matches.
- Machine values (the notion-api path) live in `config.md`; the CLI
  reads it at run time.

## Dependencies
- notion (bin/notion-api) — all Notion reads/writes go through it; never reimplement auth
- todo-find (bin/find-todo) — locating the todo a completion or update belongs to
- todo-file (SKILL.md) — the body-writing rules for edits to existing bodies
- jeep-log (~/workspace/custom-skills/jeep-log) — Jeep-project completions that are work on the Jeep are logged to the Jeep Service Log through it
- record-learning (bin/record-learning) — learning loop

## Learning loop

Owned by the record-learning skill (see Dependencies). Record with
`~/workspace/custom-skills/record-learning/bin/record-learning todo-update "<learning>"`.
