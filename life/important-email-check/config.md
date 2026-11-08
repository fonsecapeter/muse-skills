# important-email-check config

Machine values for `bin/scan-inbox`. The script reads the fenced JSON
block at run time — never hardcode these in scripts or prose.

```json
{
  "window_hours": 26,
  "max_results": 60,
  "gmail_query": "in:inbox newer_than:2d -category:promotions -category:social -label:spam",
  "watch_senders": [
    "chase.com", "usbank.com", "wellsfargo.com", "geico.com", "pge.com",
    "united.com", "nationwide.com", "petinsurance.com", "missionpet.com",
    "nivi.it", "apartments.com", "honeycomb.com", "firstam.com",
    "boulevard", "china-consulate", "consulate"
  ],
  "watch_terms": [
    "payment due", "autopay", "auto pay", "payment failed", "action required",
    "verify your", "fraud", "security alert", "appointment", "confirmation",
    "cancelled", "canceled", "refund", "deadline", "expires", "expiring",
    "overdue", "past due", "claim", "invoice", "statement ready",
    "delivery", "shipped", "reservation"
  ],
  "exclude_senders": [
    "no-reply@compass.com"
  ],
  "exclude_terms": [
    "unsubscribe", "% off", "sale ends", "deal of the day", "newsletter",
    "webinar", "podcast"
  ]
}
```

Notes:
- `window_hours` is 26, not 24, so consecutive daily runs overlap
  slightly instead of leaving a gap. The Gmail query pulls 2 days and
  the script filters to the window by timestamp.
- The query drops Gmail's Promotions/Social categories up front.
  Updates stays IN — bills, statements, and autopay notices land there
  (the GEICO autopay email was categorized Updates; an early version of
  this query excluded it and the scan missed a payment notice —
  caught in the 2026-10-13 live test).
  the agent's judgment in SKILL.md is the real importance filter —
  `watch_senders`/`watch_terms` only nominate candidates.
- Tune the watch lists here, never in the script.
