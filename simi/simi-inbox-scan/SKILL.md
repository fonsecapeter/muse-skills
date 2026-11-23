# simi-inbox-scan

The email layer for Simi's claims: watch Gmail for new Mission Pet
Hospital invoices and hand each new invoice PDF to the staging step.
Staging mechanics belong to the simi-stage-invoice skill; the state
machine and row statuses belong to the simi-claims skill.

## How it works

`bin/scan-inbox` (no args):

1. Searches Gmail for the configured sender query.
2. Skips messages already seen (state file).
3. Lists each message's attachments and applies the filename filter
   (config `filename_include` / `filename_exclude`): invoice PDFs
   pass, vaccination/rabies certificates and patient charts are
   reported as filtered out, not stored. Charts have their own rule
   (`records/charts`, dated name) — see the simi-claims skill.
4. Downloads each passing attachment, hashes it (sha256), skips bytes
   already stored (Mission Pet Hospital sends duplicates).
5. Extracts invoice number/date/total via the simi-stage-invoice
   `bin/extract-invoice` CLI and checks the idempotency snapshots:
   invoice numbers already in the spreadsheet, filenames already in
   the todo OR processed Drive folders. Anything already captured is
   reported, not re-staged — safe even after Peter moves filed PDFs
   to the processed folder.
6. Lines it up — only when the invoice is genuinely new. "Captured"
   means the spreadsheet already has a row for it (invoice number, or
   date+total match): the sheet is the source of truth, so a row
   alone means handled — never re-upload on a row match (source
   filenames vary; re-uploading would dupe). If the dated file is
   staged but the row is missing, only the row is healed. Otherwise
   it uploads the PDF to `invoices/todo` as
   `invoice_yyyy_mm_dd_<invoice_id>.pdf` (via simi-stage-invoice
   `bin/upload-invoice --folder`) and appends the `todo` row (via
   simi-claims `bin/log-claim`) as one atomic unit: both writes
   verified before moving on, and a half-done invoice stays unmarked
   so the next run retries it. A local backup copy goes to
   `~/workspace/simi-claims/work/`.
7. Updates the state file and prints a JSON report (`lined_up`,
   `already_captured`, `incomplete`, `duplicates_skipped`,
   `filtered_out`, `messages_scanned`).

Run it on demand or from a cron one-liner. The important-email-check
also runs it when it spots a Mission Pet Hospital invoice, so new
invoices get lined up as soon as Peter hears about them. It is
idempotent: reruns find nothing new, and already-filed invoices are
never re-staged.

The standing three-way verifier is the simi-reconcile skill.

When a run lines up a new invoice, the message to Peter includes the
invoice PDF and the Nationwide login link
(https://my.petinsurance.com/login) — that's his cue to file, per his
`invoice_processing` doc.

## Standing rules

- Read-only against Gmail: search + download only. Drive uploads and
  spreadsheet rows are the skill's lined-up output — that's the job
  Peter asked for, nothing else gets written.
- Never invent message ids, hashes, invoice numbers, or dates —
  everything comes from the API or the extracted PDF.
- Talk plain: no commands, ids, or JSON in replies.

## Dependencies

- record-learning (bin/record-learning) — learning loop
- simi-stage-invoice (bin/extract-invoice) — extract invoice
  number/date/total
- simi-stage-invoice (bin/upload-invoice) — upload dated PDF to Drive
  folder
- simi-claims (bin/log-claim) — append todo spreadsheet row
- gmail (external hatch_gws_cli) — search MPH emails, download
  attachments
- google_drive (external hatch_gws_cli) — idempotency folder listings
- google_sheets (external hatch_gws_cli) — idempotency row check

## Learning loop

Owned by the record-learning skill (see Dependencies). Record with
`~/workspace/custom-skills/record-learning/bin/record-learning simi-inbox-scan "<learning>"`.
