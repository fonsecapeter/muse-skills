# simi-claims

The model for Simi's Nationwide pet-insurance claims: the state
machine, the claim-identity rules, the plan terms, and the shared
config the other Simi skills read. The action skills do the work and
defer to this skill for the model:

- `simi-inbox-scan` — watches Gmail for new invoice emails
- `simi-stage-invoice` — stages an invoice PDF into Drive + the sheet
- `simi-log-filing` — logs a claim Peter filed
- `simi-close-claim` — records the claim id and payment, closes the row
- `simi-reconcile` — verifies Gmail, Drive, and the sheet agree

Peter's `invoice_processing` Google Doc in the Vet folder is the
canonical handoff doc — this model mirrors it.

## The state machine

```
todo ── Peter files in the portal ──▶ submitted ── Peter deposits the check ──▶ processed
```

- `todo` — invoice captured: PDF in `invoices/todo`, row logged.
- `doing` — Peter is filing in the portal. A quick step, optional to
  track.
- `submitted` — Peter has filed. submitted_date is the filing date,
  set from his chat report, and the PDF moves to
  `invoices/processed`. A filed claim takes a couple of days to
  appear in the portal, so the row carries no claim_id yet — the
  claim id is recorded at close-out.
- `processed` — Peter has deposited the check: claim_id and
  amount_paid are filled.

The sheet's status column enforces these four values with a strict
dropdown (config `status_values`). Rows added later do not inherit
the validation automatically — apply it to new rows when adding them.

## Who does what

- **Peter** files each claim himself at https://my.petinsurance.com.
  He sends a screenshot of what he filed (form + confirmation), later
  the claim-details screenshot, and a photo of the paper record when
  he deposits the check.
- **Tony** stages invoices, keeps the sheet and Drive in line with
  each filing, archives the claim-details screenshots, and fills the
  row at close-out.
- Filing screenshots are working evidence for logging — they are not
  saved. Only claim-details screenshots are archived (simi-close-claim).

## The model (set by Peter 2026-11-05)

- Every vet visit has an invoice email with a PDF carrying a unique
  invoice id. That PDF belongs in Drive and gets exactly one
  spreadsheet row. Rows are keyed by invoice_id (MPH) and carry the
  Nationwide claim_id once the claim is closed out.
- **The Nationwide portal is the only source of truth for whether a
  claim was submitted.** A submitted claim exists in the portal with a
  claim id, a treatment date, a submitted date, and an amount; match
  invoice ↔ claim on treatment date + amount. Receipt emails are
  ignored — do not use them as evidence either way. Memory and
  inference ("it was probably filed") are not evidence either.
- **Claim identity is the details-page amount + treatment date, never
  elimination.** One filing can spawn a duplicate $0 claim record with
  its own claim id (Apr 2024: #2024040503712, a zeroed duplicate of the
  dental claim — not a filing of invoice #295608, which has no valid
  claim). "Only two unfiled invoices in the window" proves nothing.
  And the portal's History cards are unreliable for amount — a card
  can show 'Pending' where the details page shows $0.00 — so always
  read the claim's details page, never the card.
- The sheet's columns (Peter's order, set 2026-11-05) are invoice_id,
  claim_id, treatment_date, submitted_date, status, cost,
  amount_paid, location, what, notes — sorted by treatment_date,
  newest at the bottom. Location codes Peter uses: `MPH` (Mission Pet
  Hospital), `VCA`, `SFAMC`, `DVD`. invoice_id is filled for MPH only;
  other locations leave it blank (Peter's call, 2026-11-05).
- The Drive layout under `Vet` is the contract: `invoices/todo` holds
  captured invoices, `invoices/processed` is the archive for filed
  invoices, `claims` holds the claim-details screenshots, and
  `records/charts` holds patient charts. Folder ids live in this
  skill's config.

## Plan knowledge

Policy C-2560724. At the 2026-03-24 renewal it moved from the Major
Medical Plan + Pet Wellness Plus rider (benefit schedule) to Modular
Pet Insurance — so split every estimate by treatment date against
the renewal:

- *Before 2026-03-24 (Major Medical):* benefit-schedule plan:
  allowances are per condition/procedure per policy year, reset
  ~Mar/Apr — no monthly caps. $250 deductible once per policy year.
  Prescription meds bill against the condition's allowance;
  preventive (flea/tick/heartworm) against the wellness rider's
  annual limit ($75/yr prevention, $75/yr vaccinations).
  Echocardiogram allowance $440/yr. Vetmedin pays in full under
  Valvular Heart Disease, no cap in sight; minor diagnosis lines pay
  at billed.
- *From 2026-03-24 (Modular):* medical pays 50% after a $250 per-term
  deductible; illness limit $5,000 per year. Wellness Level 1 at 100%:
  prevention $100/yr, exam $80, vaccines $80.
- **Filing window** (form VS-G-15-CA §14): prompt notice within 90
  days of first treatment; a claim submitted more than 12 months
  after the first treatment date will not be covered.
- Declarations packet: `policy_declarations_2026_02_25.pdf` in the
  Drive Vet folder.

## Judgment calls (the model's part)

- **Classification (`what` column).** Map line items to Peter's
  vocabulary: cardiac work → `cardio ultrasound` / `cardiologist`;
  meds → the med name (`vetmedin`, `simparica`); routine → `checkup`,
  `vaccinations`. Combine with ` + ` when one visit covers two things
  (`cardiac ultrasound + bloodwork`). When genuinely ambiguous, ask
  Peter in chat — never guess a medical classification.
- **Which PDFs are claims.** Invoice PDFs only. A `Patient chart.pdf`
  is supporting medical history, not a claim — save it to the
  `records/charts` folder under Vet as
  `simi_<provider>_chart_yyyy-mm-dd.pdf` (`mph` for Mission Pet
  Hospital; tag other vets like `sfamc`) and keep it out of the claim
  pipeline.
- **When to attach the chart to a Nationwide filing** (front-desk
  rule, 2026-10-08): include the chart for bigger medical procedures
  (ultrasounds, cardiology, surgery, diagnostics). Skip it for simple
  prescription fills and vaccine-only visits.
- **Duplicates.** Same bytes = same claim. Report and skip.

## Standing rules

- Read-only by default: reading Gmail/Drive/Sheets is fine. Uploading
  the renamed PDF and appending the spreadsheet row need Peter's
  explicit ask for that claim — his "process this one" counts.
- Filing on Nationwide always needs Peter's go-ahead on the exact
  claim content. Never file silently.
- CLIs fail loudly, never silently. Every CLI exits non-zero with a
  stderr message on any failed parse or unconfirmed write, and
  validates its results (return code + parsed fields) before
  reporting success — never prints success from a parsed error body.
  Callers treat a loud failure as "not captured, retry next run."
- Drive uploads go through simi-stage-invoice's `bin/upload-invoice`
  only — never raw `drive files create`: it silently ignores
  name/parent metadata, so the file lands in the wrong folder named
  "Untitled."
- **Label the verification level.** State what each pile was actually
  checked against before calling it verified, and keep verified and
  not-yet-verified items in separate lists so an unconfirmed item
  never reads as clean.
- Talk plain: no commands, ids, or JSON in replies.

## Dependencies

- record-learning (bin/record-learning) — learning loop
- google_sheets (external hatch_gws_cli) — bin/log-claim appends the
  tracking row the action skills log through

## Learning loop

Owned by the record-learning skill (see Dependencies). Record with
`~/workspace/custom-skills/record-learning/bin/record-learning simi-claims "<learning>"`.
