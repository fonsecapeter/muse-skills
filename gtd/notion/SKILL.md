---
name: "notion"
description: "Use Notion when the user asks for Notion or this provider's API."
---

# Notion

## Purpose
Peter's Notion workspace: TODO database + Projects. Two access paths exist —
use the right one (see "Which path" below).

## Which path to use
- **Cron scripts** (gtd-counts, due-todos, todo-summary):
  `bin/notion-api` — the custom REST integration. It has no usage caps and
  is what the morning crons depend on. These stay on it unless Peter
  says otherwise.
- **Interactive / agentic work** (searching, reading pages, one-off lookups):
  `bin/notion-query` — the official Notion connector (MCP). Better for
  exploration, but its `query_data_sources` operation is usage-capped by
  Notion and the cap is easy to hit (~10 queries exhausted it on
  2026-09-29). Search and fetch are not capped.

## Tooling
`bin/notion-api` (custom REST; other skills' CLIs call this, never reimplement):
`bin/notion-query` (official MCP; SQL over collection URLs):

```sh
bin/notion-api GET /users/me                      # auth check
bin/notion-api GET /databases/<database_id>       # schema
bin/notion-api POST /databases/<database_id>/query \
  --data '{"filter":{"property":"Status","status":{"does_not_equal":"Done"}},"page_size":100}'
```

```sh
bin/notion-query <database-id | collection-url> "<sql>"
# e.g. bin/notion-query 8ca2abf0828642019c4747d69eb65a71 \
#   'SELECT Task, Status FROM "{collection}" WHERE Status = '"'"'TODO'"'"' LIMIT 10'
# {collection} is replaced with the resolved collection URL. Database UUIDs
# are resolved via notion-fetch and cached in bin/.collection-cache.json.
# For search/fetch/one-off reads, `notion-cli` (see /opt/hatch/skills/notion/SKILL.md)
# can also be used directly.
```

## TODO / Projects schema (as of 2026-09-29)
- TODO db id: `8ca2abf0828642019c4747d69eb65a71` — `Task` (title), `Status` (status: TODO / Parked / Doing / Done / Not Doing), `Project` (relation), `Priority` (select P0/P1/P2), `Due` (date), `Blocked by`/`Blocking` (self-relations). Button props `Park`, `Doing`, `Done`, `Revive` set Status in the UI — set `Status` directly via API instead.
- Projects db id: `db1d8746-4de1-4cd9-9cf6-9c44accbfa89` — title prop is `Project`; status options: To Do / Waiting / Doing / Done / Not Doing. Set a todo's project via `Project.relation: [{id: <project page id>}]`.
- Peter's convention: **title = the action to take**; details go in the page body (via `PATCH /blocks/<page_id>/children`) only if needed. Logistics stay out of titles.
- Priority: P0 = top, P1 = default, P2 = lower — leave unset on new todos; Peter triages himself. A due date is a real commitment.
- Status meanings live in the system map (`~/workspace/custom-skills/SYSTEM.md`).
- Umbrella and step todos cross-link both ways.

## Operating Rules
1. Read-only by default — only write when Peter explicitly asks.
2. Requests go to api.notion.com only.
3. Peter processes his own intake; items move between Google Tasks and Notion only when he asks.
4. Chat report = completion signal: when Peter reports in chat that a todo is done, that report stands as the "asked for the change" case for that todo. The mechanics are owned by the **todo-update** skill; follow it. This skill is plumbing only.

## Dependencies
- record-learning (bin/record-learning) — learning loop

## Learning loop

Owned by the record-learning skill (see Dependencies). Record with
`~/workspace/custom-skills/record-learning/bin/record-learning notion "<learning>"`.
