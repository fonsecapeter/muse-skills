---
name: "date-idea-save"
description: "Save a date idea"
---

# Date Idea Save

Saves a new date idea for Peter and Neha as a row in the "Date Ideas"
database in Notion (under "Neha Stuff", modeled on the TODO
database). Machine values live in `config.json`, which the CLI
parses directly: the database id, the default Type, and the path to
the notion skill's `bin/notion-api`, which all Notion access defers
to. Marking an idea done is the date-idea-done skill's job.

## The row

- **Idea** (title): the name, short and lowercase, matching the
  existing rows: "horse date", "farmhouse inn".
- **Link** (url): the maps or product link. An idea can have no link.
- **Type** (select): `Day`, `Weekend away`, or `Wineries`. Default
  is `Day`; use `Weekend away` for overnight trips and `Wineries`
  for winery visits.
- **Notes** (rich text): a short trailing note, when there is one
  ("nostalgic beach, restaurants and shopping"). Anything longer
  goes in the row's page body.
- **Status** starts at `TODO`.

## Save

1. Run `bin/add-idea "<name>" "<url>"` in this skill's directory,
   with `--type "<Type>"` when the default does not fit and
   `--notes "<note>"` when there is a trailing note. The URL can be
   omitted for an idea with no link. The CLI refuses a name that is
   already in the database and verifies the new row before
   printing it.
2. Report back with the name and type, one line.

## Dependencies
- notion (bin/notion-api) — all Notion reads/writes go through it; never reimplement auth
- record-learning (bin/record-learning) — learning loop

## Learning loop

Owned by the record-learning skill (see Dependencies). Record with
`~/workspace/custom-skills/record-learning/bin/record-learning date-idea-save "<learning>"`.
