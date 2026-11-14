# simi-claims config

Machine values for `bin/`. Scripts read the fenced JSON block at run time —
never hardcode these in scripts or prose.

```json
{
  "drive_folder_id": "1XhZ2aniyVW6gWzEJAyCKGlItdM_gKgmK",
  "drive_folder_name": "invoices/processed",
  "invoices_folder_id": "1gMeiByJM95F3DBklCFjvPB3yJGIT0302",
  "todo_folder_id": "1V9ZOnOncsjea649s1wIZ61L7Jnpb13IL",
  "vet_folder_id": "1F250Z3A_OJnJUDUspXVm3kdG9PQOEET8",
  "chart_filename_pattern": "simi_<provider>_chart_yyyy-mm-dd.pdf",
  "spreadsheet_id": "1lKbPwrv8UqlSOGuUqveHTd-a3UOZBtxg_iUGqnFjcnM",
  "spreadsheet_tab": "Sheet1",
  "claims_folder_id": "1DdCjz4otSUJoJUqaiArFRVPjh-BUAxD3",
  "sheet_columns": ["invoice_id", "claim_id", "treatment_date", "submitted_date", "status", "cost", "amount_paid", "location", "what", "notes"],
  "claim_email_sender": "missionpethospital@gmail.com",
  "nationwide_claims_url": "https://my.petinsurance.com/login",
  "plan": "Modular Pet Insurance (from 2026-03-24 renewal; Major Medical Plan + Pet Wellness Plus Rider before)",
  "plan_policy_number": "C-2560724",
  "plan_renewal_date": "2026-03-24",
  "annual_deductible": 250,
  "medical_coinsurance": 0.5,
  "illness_limit_per_year": 5000,
  "wellness_level": "Level 1",
  "wellness_prevention_cap_per_year": 100,
  "wellness_exam_cap_per_year": 80,
  "wellness_vaccines_cap_per_year": 80,
  "filing_deadline_months": 12,
  "prompt_notice_days": 90,
  "policy_form": "VS-G-15-CA",
  "timezone": "America/Los_Angeles",
  "filename_pattern": "invoice_yyyy_mm_dd_<invoice_id>.pdf",
  "status_values": ["todo", "submitted", "processed"]
}
```

Notes:
- `plan` (set 2026-11-12, from the declarations packet
  `policy_declarations_2026_02_25.pdf` in the Drive Vet folder):
  policy C-2560724 moved from Major Medical to Modular Pet
  Insurance at the 2026-03-24 renewal. Estimates split by treatment
  date against the renewal: before it, the old benefit schedule;
  from it, 50% medical co-insurance after the $250 deductible,
  $5,000/yr illness limit, Wellness Level 1. Filing window (form
  VS-G-15-CA §14): prompt notice within 90 days, hard cutoff at
  12 months after first treatment.
- `filename_pattern`: `invoice_yyyy_mm_dd_<invoice_id>.pdf` — date and
  invoice number, per Peter's `invoice_processing` doc (set 2026-11-05;
  all existing PDFs were renamed to match in the restructure).
- `status_values` (model set 2026-11-05): `todo` = invoice captured
  (PDF in `invoices/todo` + row logged), not yet filed;
  `submitted` = claim exists in Nationwide (claim_id + submitted_date
  filled from the portal; PDF moved to `invoices/processed`);
  `processed` = Peter deposited the check and amount_paid is filled.
- The sheet's data starts at row 3 (row 1 blank, row 2 headers at
  B2:K2, Peter's "Steps to process" block lives at L2:L5). Rows are
  sorted by treatment_date, newest at the bottom. Append new rows
  below the last data row.
- `invoice_id` is filled for MPH rows only (blank for other locations,
  per Peter 2026-11-05). `claim_id` and `submitted_date` come from the
  Nationwide portal — the portal is the source of truth for whether a
  claim was submitted; receipt emails are not used.
