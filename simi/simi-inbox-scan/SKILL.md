# simi-inbox-scan

Watch Gmail for new Mission Pet Hospital invoices and line them up for
Peter — one skill, one job: Gmail in, invoice PDFs lined up in Drive plus
a `todo` spreadsheet row. The simi-claims skill owns the row from
there (Peter's `invoice_processing` doc is the canonical handoff).

## How it works

`bin/scan-inbox` (no args):

1. Searches Gmail for the configured sender query.
2. Skips messages already seen (state file).
3. Lists each message's attachments and applies the filename filter
   (config `filename_include` / `filename_exclude`): invoice PDFs pass,
   vaccination/rabies certificates and patient charts are reported as
   filtered out, not stored. Charts have their own rule
   (`records/charts`, dated name) — see the simi-claims skill.
4. Downloads each passing attachment, hashes it (sha256), skips bytes
   already stored (Mission Pet Hospital sends duplicates).
5. Extracts invoice number/date/total via the simi-claims
   `bin/extract-invoice` CLI and checks the idempotency snapshots:
   invoice numbers already in the spreadsheet, filenames already in the
   todo OR processed Drive folders. Anything already captured is
   reported, not re-staged — safe even after Peter moves filed PDFs to
   the processed folder.
6. Lines it up — only when the invoice is genuinely new. "Captured"
   means the spreadsheet already has a row for it (invoice number, or
   date+total match): the sheet is the source of truth, so a row alone
   means handled — never re-upload on a row match (source filenames
   vary; re-uploading would dupe). If the dated file is staged but the
   row is missing, only the row is healed. Otherwise it uploads the PDF
   to `invoices/todo` as `invoice_yyyy_mm_dd_<invoice_id>.pdf` (via
   simi-claims `bin/upload-invoice --folder`) and appends the `todo`
   row (via `bin/log-claim`) as one atomic unit: both writes verified
   before moving on, and a half-done invoice stays unmarked so the next
   run retries it. A local backup copy goes to
   `~/workspace/simi-claims/work/`.
7. Updates the state file and prints a JSON report (`lined_up`,
   `already_captured`, `incomplete`, `duplicates_skipped`,
   `filtered_out`, `messages_scanned`).

Run it on demand or from a cron one-liner. The important-email-check also runs it when it spots a Mission Pet Hospital invoice, so new invoices get lined up as soon as Peter hears about them. It is idempotent: reruns find
nothing new, and already-filed invoices are never re-staged.

## Reconcile

`bin/reconcile` (no args) — the standing verifier. Three-way
reconciliation across ALL Mission Pet Hospital emails, both Drive
folders, and the spreadsheet:

- Phase 1 builds exact content indexes from the PDFs themselves (invoice
  number and date+total per file — filename guessing can't fool it), then
  for each Gmail invoice: captured in both → skip; in neither → line up
  (atomic per invoice); in Drive but not the sheet → heal the row; in
  the sheet but not Drive → heal the upload.
- Phase 2 re-reads everything fresh and verifies: each todo-folder PDF's
  extracted date matches its filename (misnamed files are renamed),
  every file pairs to a row (missing rows are healed from the extracted
  data), invoice numbers and byte hashes are unique — two invoices on
  the same day are fine when numbers and amounts differ — every todo
  row pairs to a file, and the processed folder is scanned for duplicate
  invoice numbers.

Idempotent: reruns find nothing new.

Heal-uploads land where the row's status says the PDF belongs:
filed claims (`submitted`/`processed`) go to the processed folder,
never back into todo. Phase 2 re-reads both folders fresh, so a heal
the run just made is visible to the verification that follows — a
stale folder read once re-uploaded filed invoices into todo as
duplicates.

## The handoff

The Drive layout under `Vet`, plus the spreadsheet's status column,
is the contract with Peter:

- `invoices/todo` — this skill lines new invoices up here with `todo`
  spreadsheet rows.
- `invoices/processed` — the archive for filed invoices. Tony moves
  the PDF here when the claim is submitted; the row closes out as
  `processed` when the check is deposited.
- `claims` — Nationwide claim-details screenshots (simi-claims skill).
- The old `unprocessed_invoices`, `vet invoices`, and
  `probably_submitted` folders were retired and trashed 2026-11-05 in
  the restructure to this layout.

When a run lines up a new invoice, the message to Peter includes the
invoice PDF and the Nationwide login link
(https://my.petinsurance.com/login) — that's his cue to file, per his
`invoice_processing` doc.

Row statuses (`todo` → `submitted` → `processed`) are defined in the
simi-claims skill's model — it is the single source for them.

## Standing rules

- Read-only against Gmail: search + download only. Drive uploads and
  spreadsheet rows are the skill's lined-up output — that's the job Peter
  asked for, nothing else gets written.
- Never invent message ids, hashes, invoice numbers, or dates — everything
  comes from the API or the extracted PDF.
- Talk plain: no commands, ids, or JSON in replies.

## Dependencies

- record-learning (bin/record-learning) — learning loop
- simi-claims (bin/extract-invoice) — extract invoice number/date/total
- simi-claims (bin/upload-invoice) — upload dated PDF to Drive folder
- simi-claims (bin/log-claim) — append todo spreadsheet row
- gmail (external hatch_gws_cli) — search MPH emails, download attachments
- google_drive (external hatch_gws_cli) — idempotency folder listings
- google_sheets (external hatch_gws_cli) — idempotency row check

## Learning loop

Owned by the record-learning skill (see Dependencies). Record with
`~/workspace/custom-skills/record-learning/bin/record-learning simi-inbox-scan "<learning>"`.
