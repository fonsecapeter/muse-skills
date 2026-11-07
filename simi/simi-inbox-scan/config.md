# simi-inbox-scan config

Machine values for `bin/scan-inbox`. The script reads the fenced JSON block
at run time — never hardcode these in scripts or prose.

```json
{
  "gmail_sender": "missionpethospital@gmail.com",
  "gmail_query": "from:missionpethospital@gmail.com",
  "unprocessed_folder_id": "1V9ZOnOncsjea649s1wIZ61L7Jnpb13IL",
  "state_file": "~/workspace/custom-skills/simi-inbox-scan/state.json",
  "max_results": 25,
  "filename_include": ["invoice"],
  "filename_exclude": ["vaccination", "rabies", "certificate", "chart"]
}
```

Notes:
- `unprocessed_folder_id` is the Drive `invoices/todo` folder (under
  `Vet/invoices`; the key name is historical). New invoices are uploaded
  here as `invoice_yyyy_mm_dd_<invoice_id>.pdf` — this is how they're
  lined up for Peter.
- The old `unprocessed_invoices`, `vet invoices`, and
  `probably_submitted` folders were retired and trashed 2026-11-05 in
  the restructure to `invoices/todo` + `invoices/processed`
  (submission is settled against the Nationwide portal, not by triage).
- `state.json` holds `seen_message_ids` and `stored_sha256s` for dedupe
  across runs. The local `~/workspace/simi-claims/inbox/` dir is retired;
  the Drive folder is the handoff now.
