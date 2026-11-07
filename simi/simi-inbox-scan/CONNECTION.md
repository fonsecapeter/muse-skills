# simi-inbox-scan — CONNECTION

How this skill connects to Peter's systems.

## Gmail

Through the vendored Google Workspace CLI (`hatch_gws_cli`), same as the
other skills. `hatch_gws_cli gmail status` must be `connected` (verified
2026-10-08). If not connected, follow the gmail skill's SKILL.md connect
flow — never invent a URL or ask for credentials.

This skill is read-only against Gmail: it searches and downloads
attachments. Its writes are the lined-up output — the dated PDF into the
Drive `invoices/todo` folder and the `todo` spreadsheet row
(via the simi-claims CLIs), plus a local backup copy in
`~/workspace/simi-claims/work/`. It never writes back to Gmail.

## Learning loop

Owned by the record-learning skill (see Dependencies). Record with
`~/workspace/custom-skills/record-learning/bin/record-learning simi-inbox-scan "<learning>"`.
