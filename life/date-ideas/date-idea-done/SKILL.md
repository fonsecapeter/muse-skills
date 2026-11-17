---
name: "date-idea-done"
description: "Mark a date idea done"
---

# Date Idea Done

Marks a date idea done in the "Date Ideas" database in Notion
(under "Neha Stuff", modeled on the TODO database). Done means the
row's **Status** becomes `Done` and its **Went** date is set to the
day they went; the row stays in the database. Machine values live
in `config.json`, which the CLI parses directly: the database id
and the path to the notion skill's `bin/notion-api`. All Notion
access defers to that CLI. Saving a new idea is the
date-idea-save skill's job.

## Mark done

1. Run `bin/check-idea "<name fragment>"` in this skill's directory.
   It sets Status to Done and Went to today (Peter's timezone) on
   the one matching row, and verifies the new state. Zero or
   multiple matches fail loudly; on multiple matches, rerun with a
   longer fragment.
2. Report back with the idea's name, one line.

## Dependencies
- notion (bin/notion-api) — all Notion reads/writes go through it; never reimplement auth
- record-learning (bin/record-learning) — learning loop

## Learning loop

Owned by the record-learning skill (see Dependencies). Record with
`~/workspace/custom-skills/record-learning/bin/record-learning date-idea-done "<learning>"`.
