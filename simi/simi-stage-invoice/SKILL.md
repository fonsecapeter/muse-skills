# simi-stage-invoice

Stage one Simi vet invoice: extract its fields, dedupe it, rename it,
upload it to Drive, and append its `todo` row to the tracking sheet.
The state machine, the classification vocabulary, and the shared
values live in the simi-claims skill — this skill defers to its
config and model.

## Steps (one invoice PDF)

1. **Extract** — `bin/extract-invoice <pdf>` → invoice number, date,
   total, line items. Sanity-check the numbers against the PDF text
   before trusting them.
2. **Dedupe** — `bin/dedupe-check <pdf>` → name/size collisions in the
   Drive folder. A collision with identical size is a duplicate: stop
   and say so. Mission Pet Hospital sometimes sends the same PDF
   twice.
3. **Rename** — `invoice_yyyy_mm_dd_<invoice_id>.pdf` from the invoice
   date + invoice number (simi-claims config `filename_pattern`).
4. **Upload** — `bin/upload-invoice <pdf> <dest_name> --folder <id>`
   into the `invoices/todo` folder (folder ids in the simi-claims
   config).
5. **Log** — simi-claims `bin/log-claim --date … --location … --cost …
   --what … --invoice-id …` appends the tracking row at status `todo`.
   The `what` classification follows the vocabulary in the simi-claims
   model.

`simi-inbox-scan` runs these steps for emailed invoices. Run them
directly when Peter hands Tony an invoice PDF — his "process this
one" is the go-ahead for the upload and the row.

The invoice parser (`bin/invoice_parse.py`) carries unit tests —
`bin/test` in this skill runs them against real invoice fixtures.

## Dependencies

- record-learning (bin/record-learning) — learning loop
- simi-claims (bin/log-claim) — append the tracking row
- simi-claims (config.md) — folder ids, filename pattern, sheet id
- google_drive (external hatch_gws_cli) — dedupe check, upload the
  renamed invoice
- google_sheets (external hatch_gws_cli) — the row append, via
  bin/log-claim

## Learning loop

Owned by the record-learning skill (see Dependencies). Record with
`~/workspace/custom-skills/record-learning/bin/record-learning simi-stage-invoice "<learning>"`.
