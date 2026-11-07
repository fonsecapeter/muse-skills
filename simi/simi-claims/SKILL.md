# simi-claims

Simi's Nationwide pet-insurance claim toolkit: deterministic CLIs for
invoice extraction, Drive upload, and spreadsheet logging, plus the
judgment calls (classification, chart rule, plan knowledge) for lining
claims up. The `simi-inbox-scan` skill drives the Gmail watch and calls
these CLIs to line new invoices up in the Drive `invoices/todo`
folder with `todo` spreadsheet rows. Peter files on Nationwide himself
(the portal blocks automated browsers); the row then gets the claim's
id and submitted date from the portal (status `submitted`) and the PDF
moves to `invoices/processed`; when he deposits the check and sends a
photo of the paper record, the row flips to `processed` with
amount_paid filled. The canonical handoff doc is Peter's
`invoice_processing` Google Doc in the Vet folder — this pipeline
mirrors it.

## The pipeline (one invoice PDF)

1. **Extract** — `bin/extract-invoice <pdf>` → invoice number, date,
   total, line items. Sanity-check the numbers against the PDF text before
   trusting them.
2. **Dedupe** — `bin/dedupe-check <pdf>` → name/size collisions in the
   Drive folder. A collision with identical size is a duplicate: stop and
   say so. Mission Pet Hospital sometimes sends the same PDF twice.
3. **Rename** — `invoice_yyyy_mm_dd_<invoice_id>.pdf` from the invoice
   date + invoice number (config `filename_pattern`).
4. **Upload** — `bin/upload-invoice <pdf> <dest_name> [--folder <id>]`
   into the Drive folder (default: `invoices/processed`; the scanner
   passes the `invoices/todo` folder id).
5. **Log** — `bin/log-claim --date … --location … --cost … --what …
   --invoice-id …` appends the tracking row (status `todo`). The sheet's
   columns (Peter's order, set 2026-11-05) are invoice_id, claim_id,
   treatment_date, submitted_date, status, cost, amount_paid, location,
   what, notes — sorted by treatment_date, newest at
   the bottom. Location codes Peter uses: `MPH` (Mission Pet Hospital),
   `VCA`, `SFAMC`, `DVD`. invoice_id is filled for MPH only; other
   locations leave it blank (Peter's call, 2026-11-05).
6. **File on Nationwide** — Peter does this himself at
   https://my.petinsurance.com (automated browsers are blocked). Once
   the claim exists in the portal, fill the row's claim_id and
   submitted_date from the portal, set status `submitted`, and move
   the PDF from `invoices/todo` to `invoices/processed`.
7. **Claim screenshot** — after filing, Peter sends a screenshot of the
   claim's Nationwide details page. Save it to the Drive `claims`
   folder (config `claims_folder_id`) as
   `claim_<claim_id>_<invoice_id>.jpg` (invoice_id suffix omitted for
   non-MPH claims, which have none). The screenshot is a point-in-time
   snapshot: Nationwide keeps updating the details page as they
   process, and we do NOT re-screenshot or overwrite — our tracking
   lives in the spreadsheet. When a details screenshot shows a Paid
   amount, put it in the row's amount_paid.
8. **Close the loop** — Peter deposits the check and sends a photo of
   the paper record/check; fill amount_paid from it and set status →
   `processed`. (The PDF already moved at the submitted step.)

## The model (set by Peter 2026-11-05 — this supersedes all earlier
verification schemes, including receipt-email matching)

- Every vet visit has an invoice email with a PDF carrying a unique
  invoice id. That PDF belongs in Drive and gets exactly one
  spreadsheet row. Rows are keyed by invoice_id (MPH) and carry the
  Nationwide claim_id once filed.
- **The Nationwide portal is the only source of truth for whether a
  claim was submitted.** A submitted claim exists in the portal with a
  claim id, a treatment date, a submitted date, and an amount; match
  invoice ↔ claim on treatment date + amount. Receipt emails are
  ignored — do not use them as evidence either way. Memory and
  inference ("it was probably filed") are not evidence either.
- **Claim identity is the details-page amount + treatment date, never
  elimination.** One filing can spawn a duplicate $0 claim record with
  its own claim id and its own receipt email (evidence: Apr 2024
  #2024040503712, $0.00, a zeroed duplicate of dental claim
  #2024040503666, paid $1,460 — not the Mar 5 invoice #295608, which
  was never filed). "Only two unfiled invoices in the window" proves
  nothing. And the portal's History cards are unreliable for amount —
  a card can show 'Pending' where the details page shows $0.00 — so
  always read the claim's details page, never the card.
- Status lifecycle: `todo` (invoice captured, no claim in Nationwide)
  → `submitted` (claim in the portal, claim_id + submitted_date on the
  row) → `processed` (check deposited, amount_paid filled). For the
  2026-11-05 backlog audit Peter ruled submitted = deposited, so
  verified-submitted rows were marked closed directly (as `done`,
  renamed `processed` the same day).
- The old `pending` / `probably_uploaded` / `not_sure` statuses and the
  `probably_submitted` Drive folder are retired.

## Verification

`simi-inbox-scan`'s `bin/reconcile` is the standing verifier: three-way
reconciliation across all MPH emails, both Drive folders, and the
spreadsheet, healing gaps (missing row, missing upload) and then
re-verifying from fresh reads. It verifies capture only — whether a
claim was submitted is settled against the Nationwide portal, per the
model above. Idempotent; rerun it any time the piles look off. The
2026-11-05 backlog rebuild and restructure history lives in Simi's
memory file, not here. Current state (verified 2026-11-05): 33 rows —
18 `processed`, 15 `todo`; reconcile clean. The invoice parser
(`bin/invoice_parse.py`) carries unit tests — `bin/test` in this skill
runs them against real invoice fixtures.

## Judgment calls (the agent's part)

- **Classification (`what` column).** Map line items to Peter's vocabulary:
  cardiac work → `cardio ultrasound` / `cardiologist`; meds → the med name
  (`vetmedin`, `simparica`); routine → `checkup`, `vaccinations`. Combine
  with ` + ` when one visit covers two things
  (`cardiac ultrasound + bloodwork`). When genuinely ambiguous, ask Peter
  in chat — never guess a medical classification.
- **Which PDFs to process.** Invoice PDFs only. A `Patient chart.pdf` is
  supporting medical history, not a claim — save it to the
  `records/charts` folder under Vet as
  `simi_<provider>_chart_yyyy-mm-dd.pdf` (`mph` for Mission Pet Hospital;
  tag other vets like `sfamc`) and keep it out of the claim pipeline.
- **When to attach the chart to a Nationwide filing** (front-desk rule,
  2026-10-08): include the chart for bigger medical procedures (ultrasounds,
  cardiology, surgery, diagnostics). Skip it for simple prescription fills
  and vaccine-only visits.
- **Duplicates.** Same bytes = same claim. Report and skip.
- **Plan knowledge.** Simi is on the Major Medical Plan + Pet Wellness Plus
  rider, $250 annual deductible. It's a benefit-schedule plan: allowances
  are per condition/procedure per policy year, reset ~Mar/Apr — no monthly
  caps. Prescription meds bill against the condition's allowance; preventive
  (flea/tick/heartworm) against the wellness rider's annual limit.

## Standing rules

- Read-only by default: reading Gmail/Drive/Sheets is fine. Uploading the
  renamed PDF and appending the spreadsheet row need Peter's explicit ask
  for that claim — his "process this one" counts.
- Filing on Nationwide always needs Peter's sign-in and his go-ahead on
  the exact claim content. Never file silently. (The portal blocks
  automated browsers outright — Akamai challenge, sign-in sessions don't
  persist — so filing stays his manual step; the local pull/process flow
  and `bin/process-inbox` were retired 2026-10-09.)
- CLIs fail loudly, never silently. Every CLI exits non-zero with a
  stderr message on any failed parse or unconfirmed write, and validates
  its results (return code + parsed fields) before reporting success —
  never prints success from a parsed error body. Callers treat a loud
  failure as "not captured, retry next run."
- Drive uploads go through `bin/upload-invoice` only — never raw
  `drive files create`: it silently ignores name/parent metadata, so the
  file lands in the wrong folder named "Untitled."
- **Label the verification level.** State what each pile was actually
  checked against before calling it verified, and keep verified and
  not-yet-verified items in separate lists so an unconfirmed item never
  reads as clean.
- Talk plain: no commands, ids, or JSON in replies.

## Dependencies

- record-learning (bin/record-learning) — learning loop
- gmail (external hatch_gws_cli) — find invoice emails, download PDFs
- google_drive (external hatch_gws_cli) — dedupe check, upload renamed invoice
- google_sheets (external hatch_gws_cli) — append tracking row, update status

## Learning loop

Owned by the record-learning skill (see Dependencies). Record with
`~/workspace/custom-skills/record-learning/bin/record-learning simi-claims "<learning>"`.
