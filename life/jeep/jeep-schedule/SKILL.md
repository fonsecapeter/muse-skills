# Jeep Schedule

The Jeep Service Log model and the maintenance schedule — the shared
reference for the jeep group. This skill owns `bin/jeep-maintenance`
and `config.md`; jeep-check and jeep-log call the CLI through here.

## Governance

- Single source of truth is the spreadsheet; reminders live in Notion.
- The spreadsheet is the Jeep Service Log in Google Drive, with tabs named in `config.md`.
- A Notion todo, a chat message, and this skill group are not the record of work done.
- The Other tab's Notes column is Peter's own unstructured field, written by him when he logs work. Leave it alone — no writing, repurposing, or overwriting; the check ignores it. When logging a new row, its Notes cell stays blank unless Peter dictates a note.

## The schedule

- Read intervals and thresholds from `config.md` at run time, and read the per-item intervals from the Other tab, where each scheduled row carries its own.
- Treat a scheduled item with no actual row as never done. Its upcoming row carries the due date and mileage; baseline items are due at the current reading, which means due now.
- Count engine oil from the last row of the Oil Changes tab plus the oil interval in `config.md`, and show only the next one.
- Keep actual and due separate. A completed row carries only its Actual Date and Actual Mileage, with the Due cells blank. Each scheduled item has exactly one upcoming row — no actuals, Due (mi) and Due (date) filled — and that row is the only place due values live. The check reads Due from the upcoming row when one exists and otherwise computes it from last actual + interval. Spark Plugs are an upcoming row due at 100,000 miles, with no actual row until they're first replaced.
- Trust the Info tab's current mileage and mileage date as the odometer anchor, and surface the anchor's age in every report.
- Use these intervals, from the 2017 JK owner's manual schedule unless noted. Engine air filter every 30,000 miles, cabin air filter every 20,000 miles, spark plugs at 100,000 miles, coolant at 10 years or 150,000 miles. The per-row intervals on the Other tab are what the check actually reads.
- Jeep's schedule makes two changes conditional on severe or off-road-type use instead of giving them normal-use intervals: manual transmission fluid, at 30,000-mile points, and front and rear axle gear oil, at 40,000-mile points. Peter's dirt-road driving counts as off-road use, so both run on Jeep's conditional intervals — transmission fluid every 30,000 miles, axle gear oil every 40,000 miles.
- Use community practice where the manual gives inspections instead of intervals. Transfer case fluid every 60,000 miles, brake fluid every 3 years.
- Keep Peter's own cadences where he set them. Tire rotation every 7,500 miles or 12 months, engine oil every 7,000 miles or 12 months.

## Horizon

- The schedule is planned through the horizon end in `config.md` (2027-12-31). Peter isn't retiring the system — it just isn't solved past 2027. The check flags once that date has passed, so the schedule gets refreshed.

## Dependencies
- notion (~/workspace/custom-skills/notion/bin/notion-api) — the CLI reads the open Jeep todos through it; never reimplement auth
- google_sheets (external, /opt/hatch/bin/hatch_gws_cli) — the CLI reads and writes the Jeep Service Log through its connector CLI
- record-learning (bin/record-learning) — learning loop

## Learning loop

Owned by the record-learning skill (see Dependencies). Record with
`~/workspace/custom-skills/record-learning/bin/record-learning jeep-schedule "<learning>"`.
