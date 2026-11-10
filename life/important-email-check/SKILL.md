# Important Email Check

Peter asked for a check for anything important he may have missed.
This skill scans the recent inbox and reports only what's worth his
attention. Read-only: it never sends, archives, labels, or deletes
mail.

## Steps

1. **Collect the scan.** Run `bin/scan-inbox` in this skill's directory.
   It reads its values from `config.md` and prints JSON like
   `{"as_of": "...", "window_hours": 26, "gmail_ok": true,
   "count_total": 12, "candidates": [...], "others": [...]}`.
   Each message carries `id`, `from`, `subject`, `date`, `snippet`,
   `unread`, a Gmail link, and `hits` (which watch terms matched).
   - Gmail access defers to the gmail skill (external): `bin/scan-inbox`
     calls `hatch_gws_cli gmail` instead of reimplementing auth. See
     `CONNECTION.md`.
   - If `gmail_ok` is false, say the check couldn't reach Gmail and stop.
2. **Judge importance.** Work from `candidates` first; skim `others` for
   anything the terms missed. A message is important when it plausibly
   needs Peter to act, decide, pay, show up, or know something time-bound:
   - Action or reply needed from a real person or institution
   - Money: bills, autopay changes, failed payments, refunds, fraud or
     account-security alerts (remember: Meta account alerts are usually
     Peter's own testing — flag once, lightly)
   - Time-bound: appointments, bookings, deliveries, deadlines, expiries
   - Anything matching an open thread (China visa, HOA, mortgage, PG&E,
     GEICO/autopays, Simi claims, Palermo) that moves it forward
   - When a snippet is ambiguous, read the message
     (`hatch_gws_cli gmail +read --id <id>`) before deciding.
   - Newsletters, receipts for known purchases, marketing, and routine
     confirmations of things already handled are NOT important.
3. **Deliver the digest in chat.** Peter has ADHD and dyslexia: bullets,
   white space, short.
   - Lead with the count: "3 emails worth your eyes" (or
     similar), then one line per item: sender + what it is + why it
     matters, with the Gmail link on its own line.
   - Group by urgency when there's more than a couple: needs action /
     money / just know.
   - If nothing is important, send nothing user-visible — the check ran
     clean and silence beats noise.

## Simi vet invoices — standing handoff

If a candidate is a Mission Pet Hospital invoice email (invoice PDF
attached), don't just flag it — line it up for filing:

1. Run the simi-inbox-scan skill's `bin/scan-inbox`. It idempotently
   stages genuinely new invoices (PDF to Drive `invoices/todo`
   + a `todo` row in the Invoices spreadsheet) and reports
   already-captured ones without duplicating anything. Safe to run on
   every sighting.
2. In the digest, one line per newly lined-up invoice: date, total,
   invoice number — "New Simi invoice lined up for filing: Oct 13,
   $202.80 (#344492)." Already-captured invoices don't get a line.
   Per Peter's `invoice_processing` doc, the message also gives him
   the invoice PDF and the Nationwide login link
   (https://my.petinsurance.com/login) — that's his cue to submit.

Lining up is where Tony's part ends. This is the one standing
exception to read-only — the writes happen inside the simi pipeline
Peter designed, never to mail.

## Rules

- Plain language only. No command names, no raw JSON in the reply.
- One-time codes, passwords, and full account/card numbers from email bodies stay out of the digest — name the sender and the topic only.

## Dependencies
- gmail (external, hatch_gws_cli gmail) — reads Gmail via bin/scan-inbox; never reimplement auth
- simi-inbox-scan (bin/scan-inbox) — idempotently lines up Mission Pet Hospital invoices this check spots, so Peter can file them
- record-learning (bin/record-learning) — learning loop

## Learning loop

Owned by the record-learning skill (see Dependencies). Record with
`~/workspace/custom-skills/record-learning/bin/record-learning important-email-check "<learning>"`.
