# Jeep Log

Logging work done on Peter's 2017 Wrangler JK to the Jeep Service
Log. The row-writing rules (actual/due separation, the Notes column)
live in jeep-schedule.

## Log work and readings

- Log a job when Peter reports it done in chat, because his report is the completion signal.
- Log it with `~/workspace/custom-skills/jeep-schedule/bin/jeep-maintenance log --job "<job>" --date <YYYY-MM-DD> --miles <odometer>` — add `--parts`, `--oil` / `--filter` for an oil change, or `--type` / `--interval-mi` / `--interval-mo` for a job the sheet doesn't know yet. The command appends the actual row with the Due cells blank, rolls the item's upcoming row to the new due date and mileage, and advances the Info odometer anchor when the logged mileage is newer. Log rows change only through this command — no hand edits, and no testing it against the real sheet; `--dry-run` shows the planned writes without applying them.
- Ask for the mileage when a report has none, because the schedule math depends on it.
- The same logging applies whenever a Jeep-project Notion todo is marked Done and it represents work performed on the Jeep — scheduled maintenance or a one-off job alike: run the log command in the same turn, then close the todo. An appointment or errand todo (booking the work, buying the parts) closes without a service log. Jeep project only — no other project's completions touch the sheet.
- Mark the matching Notion Jeep todo Done after logging, following todo-update's completion flow.
- Record the transmission fluid as plain scheduled maintenance, with no extra notes.
- Update the Info tab's Current mileage and Mileage date when Peter reports a fresh odometer reading, replacing the old values. (The log command already advances the anchor when it logs work at a newer mileage.)

## Dependencies
- jeep-schedule (bin/jeep-maintenance) — the CLI and the sheet model the log writes to (config.md sits beside the CLI)
- todo-update (~/workspace/custom-skills/todo-update) — owns the completion flow for marking Jeep todos Done when Peter reports work
- record-learning (bin/record-learning) — learning loop

## Learning loop

Owned by the record-learning skill (see Dependencies). Record with
`~/workspace/custom-skills/record-learning/bin/record-learning jeep-log "<learning>"`.
