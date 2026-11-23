# simi-close-claim

Close out a filed Simi claim: record its claim_id and paid amount
from the claim-details page, and mark the row `processed` once Peter
deposits the check. The state machine and the claim-identity rules
live in the simi-claims skill; folder ids and the spreadsheet id live
in its config.

## Trigger

Peter sends a screenshot of the claim's Nationwide details page —
the first place the claim_id exists — and, once he deposits the
check, a photo of the paper record.

## Steps

1. **Save the details screenshot** to the Drive `claims` folder as
   `claim_<claim_id>_<invoice_id>.jpg` (invoice_id suffix omitted for
   non-MPH claims, which have none). The screenshot is a point-in-time
   snapshot: Nationwide keeps updating the details page as they
   process, and we do NOT re-screenshot or overwrite — our tracking
   lives in the spreadsheet.
2. **Fill the row's claim_id** from the screenshot. Match the claim
   to its invoice on the details-page amount + treatment date, never
   by elimination, and read the details page rather than the History
   card (the simi-claims model carries the full rule).
3. **Record payment.** When the details page shows a Paid amount, put
   it in the row's amount_paid.
4. **Close the row.** When Peter deposits the check and sends the
   paper-record photo, fill amount_paid from it (when the details
   page has not already set it) and set status → `processed`. The
   invoice PDF already moved at the submitted step.

## Dependencies

- record-learning (bin/record-learning) — learning loop
- simi-claims (config.md) — claims folder id, spreadsheet id, state
  machine
- google_drive (external hatch_gws_cli) — save the details screenshot
- google_sheets (external hatch_gws_cli) — fill claim_id, amount_paid,
  status

## Learning loop

Owned by the record-learning skill (see Dependencies). Record with
`~/workspace/custom-skills/record-learning/bin/record-learning simi-close-claim "<learning>"`.
