# Jeep Check

What's due on Peter's 2017 Wrangler JK, flagged from the Jeep Service
Log. The schedule and the sheet model live in jeep-schedule; this
skill runs its check.

## Run the check

- Run `~/workspace/custom-skills/jeep-schedule/bin/jeep-maintenance check` to compute what is due.
- Due dates and mileage come from the script; don't recompute them in prose.
- Deliver the script's report as the flag in the Jeep Dept side chat, exactly as printed, with the mileage anchor line kept.
- The check is read-only: no writes to the sheet or to Notion. Flag only — this skill doesn't file Notion todos for due items or mark them done.
- Report the failure in the chat when the script exits non-zero, with its stderr reason, instead of improvising a check by hand.

## Dependencies
- jeep-schedule (bin/jeep-maintenance, config.md) — the CLI, the schedule, and the sheet model this check reads
- record-learning (bin/record-learning) — learning loop

## Learning loop

Owned by the record-learning skill (see Dependencies). Record with
`~/workspace/custom-skills/record-learning/bin/record-learning jeep-check "<learning>"`.
