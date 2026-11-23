# simi-reconcile

The standing verifier for Simi's claims: three-way reconciliation
across all Mission Pet Hospital emails, both Drive invoice folders,
and the spreadsheet, healing gaps and then re-verifying from fresh
reads. It verifies capture only — whether a claim was submitted is
settled against the Nationwide portal, per the simi-claims model.
Idempotent; rerun it any time the piles look off.

## How it works

`bin/reconcile` (no args):

- Phase 1 builds exact content indexes from the PDFs themselves
  (invoice number and date+total per file — filename guessing can't
  fool it), then for each Gmail invoice: captured in both → skip; in
  neither → line up (atomic per invoice); in Drive but not the sheet
  → heal the row; in the sheet but not Drive → heal the upload.
- Phase 2 re-reads everything fresh and verifies: each todo-folder
  PDF's extracted date matches its filename (misnamed files are
  renamed), every file pairs to a row (missing rows are healed from
  the extracted data), invoice numbers and byte hashes are unique —
  two invoices on the same day are fine when numbers and amounts
  differ — every todo row pairs to a file, and the processed folder
  is scanned for duplicate invoice numbers.

Heal-uploads land where the row's status says the PDF belongs: filed
claims (`submitted`/`processed`) go to the processed folder, never
back into todo. Phase 2 re-reads both folders fresh, so a heal the
run just made is visible to the verification that follows — a stale
folder read once re-uploaded filed invoices into todo as duplicates.

Staging a healed invoice goes through the simi-stage-invoice CLIs and
simi-claims `bin/log-claim`; the email-side values (sender query,
state file) come from the simi-inbox-scan config and the sheet/Drive
values from the simi-claims config.

## Dependencies

- record-learning (bin/record-learning) — learning loop
- simi-stage-invoice (bin/extract-invoice) — extract invoice
  number/date/total for the content indexes and heals
- simi-stage-invoice (bin/upload-invoice) — heal a missing upload
- simi-claims (bin/log-claim) — heal a missing row
- simi-inbox-scan (config.md) — sender query, filename filters, state
  file
- simi-claims (config.md) — folder ids, spreadsheet id
- gmail (external hatch_gws_cli) — enumerate MPH invoice emails
- google_drive (external hatch_gws_cli) — folder listings and heals
- google_sheets (external hatch_gws_cli) — row index and heals

## Learning loop

Owned by the record-learning skill (see Dependencies). Record with
`~/workspace/custom-skills/record-learning/bin/record-learning simi-reconcile "<learning>"`.
