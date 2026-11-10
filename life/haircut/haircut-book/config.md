# Haircut book — config

Machine-readable values are in the `json` block below. Edit the values here,
not in the skill.

```json
{
  "booking_url": "https://www.joinblvd.com/b/fellow-barber/widget",
  "shop_name": "Fellow Barber - Mission District",
  "shop_address": "696 Valencia St, San Francisco, CA 94110",
  "barber": "Niamke M.",
  "barber_title": "Senior Barber II",
  "service": "Haircut",
  "service_minutes": 45,
  "service_price_usd": 80,
  "default_day": "sunday",
  "preferred_time": "16:30",
  "calendar_check_window": "4:00–6:00 PM PT",
  "suggest_latest_slot": true,
  "payment": "stripe-link",
  "typical_cadence_days": 44
}
```

## Notes

- Card hold: the service price, hold-only at booking, charged after the
  appointment. 3% surcharge on credit cards at the shop.
- The merchant-saved Visa ending 8040 is a dead card. Boulevard may
  pre-select it at checkout; the Stripe Link steer overrides it.
- Cancellation: free before 4:30 AM the day of; within 12h charged 50%;
  within 2h treated as no-show, 100%.
- Cadence (measured 2026-10-01 from past booking emails): Peter's real
  interval averages ~44 days (~6 weeks), range 38–56 days. When he asks to
  book the next one right after a cut, target ~6 weeks out unless he says
  otherwise.
- Calendar check covers Peter's calendar only — Neha's does not need to be
  free for a haircut (standing rule, 2026-10-03). Flag tight transitions —
  an event ending right before the appointment.
- Arrive 10 minutes early.
