# Notion connection

How Peter's Notion is connected. Verified against
[Notion's API docs](https://developers.notion.com) and live-tested 2026-09-11.

## Two integrations (do not confuse them)
- **"Notion Custom" (this file)** — the hand-built internal integration
  token + `bin/notion-api`. The only uncapped path; the GTD crons depend
  on it. Keep.
- **"Notion" (official Meta connector)** — connected in Peter's Muse app,
  usable from the runtime via `notion-cli` (MCP). Good for interactive
  search/fetch, but Notion caps its `query_data_sources` operation
  (exhausted after ~10 queries on 2026-09-29) — it cannot run the cron
  query workloads.

## Credential

- The stored credential (`custom.notion`) is an internal integration
  secret created at https://www.notion.com/myintegrations (Configuration
  tab → "Internal Integration Secret").
