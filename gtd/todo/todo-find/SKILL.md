---
name: "todo-find"
description: "Find a specific TODO"
---

# Todo Find

The finding layer for Peter's TODO database. Filing (todo-file) and
updating (todo-update) both start here; the notion skill owns the API
mechanics, and all Notion access defers to its `bin/notion-api`.

System map: `~/workspace/custom-skills/SYSTEM.md` — how Peter's
capture → todos → digests → completions system fits together.

## Searching

- `bin/find-todo <term> [term...]` — title search across several
  phrasings in one call; prints `[{id, title, status, due, url}]`.
  Try more than one phrasing before concluding a todo doesn't
  exist.
- Scan scope for open work is TODO / Doing / Parked. Skip Done and
  Not Doing unless Peter asks about history.

## Reading and reporting

- When a task needs more than the search row (a body checklist, the
  project, the details), read the page and its body blocks through
  `bin/notion-api` before acting or answering.
- "What's on my plate" answers come from search results, presented
  plainly: title, status, due date, project. No IDs, no raw JSON.

## Tooling

- Machine values (database IDs, the notion-api path) live in
  `config.md`; the CLI reads it at run time.

## Dependencies
- notion (bin/notion-api) — all Notion reads go through it; never reimplement auth
- record-learning (bin/record-learning) — learning loop

## Learning loop

Owned by the record-learning skill (see Dependencies). Record with
`~/workspace/custom-skills/record-learning/bin/record-learning todo-find "<learning>"`.
