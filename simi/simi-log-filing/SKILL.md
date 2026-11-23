# simi-log-filing

Log a Nationwide claim Peter just filed: mark the invoice's row
`submitted` and move its PDF to the processed folder. The state
machine lives in the simi-claims skill; folder ids and the
spreadsheet id live in its config.

## Trigger

Peter reports in chat that he filed, usually with a screenshot of
what he filed (the portal form + the confirmation). The screenshot
carries the invoice number, treatment date, and total — it is
working evidence for logging and is not saved.

A filed claim takes a couple of days to appear in the portal, so
there is no claim_id at this step. The claim id is recorded at
close-out, from the claim-details page (simi-close-claim).

## Steps

1. Identify the invoice from Peter's report or screenshot and match
   it to its sheet row — invoice_id for MPH rows, treatment date +
   amount otherwise.
2. Set the row's submitted_date to the filing date and its status to
   `submitted`.
3. Move the invoice PDF from `invoices/todo` to `invoices/processed`.
4. Read both back to verify the writes landed.

## Dependencies

- record-learning (bin/record-learning) — learning loop
- simi-claims (config.md) — folder ids, spreadsheet id, state machine
- google_drive (external hatch_gws_cli) — move the filed invoice PDF
- google_sheets (external hatch_gws_cli) — update the row

## Learning loop

Owned by the record-learning skill (see Dependencies). Record with
`~/workspace/custom-skills/record-learning/bin/record-learning simi-log-filing "<learning>"`.
