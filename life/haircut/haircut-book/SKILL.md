# Haircut Book

Book Peter's haircut at Fellow Barber (Mission, SF) with his barber
Niamke M. Barber, service, prices, and policies live in `config.md`.
Read-only until Peter confirms a slot.

## Workflow

1. **Pick the target date.** Default: the upcoming Sunday. Run
   `bin/next-sunday` in this skill's directory — it prints the date as
   YYYY-MM-DD in America/Los_Angeles (today if today is Sunday). If Peter
   names a different day, use that instead.
2. **Check his calendar.** Use the google_calendar skill's freebusy query on
   the target window from `config.md`, on his calendar only — Neha's
   calendar does not need to be free for a haircut (standing rule,
   2026-10-03). Flag anything adjacent — e.g. an event ending right before
   the shop visit.
3. **Check Niamke's availability.** Delegate to a live browser task at the
   booking URL from `config.md`; sign in via haircut-signin. Steps: sign
   in → select the barber → the service → target date → report the open
   slots in the target window.
4. **Suggest.** Present the open slots and suggest the *latest* one.
   In the suggestion itself, say explicitly that his calendar was checked
   for the target window: confirm the suggested slot fits, or name what he
   would need to move — he shouldn't have to guess whether the check
   happened. Wait for Peter's confirmation; book only on his explicit pick.
5. **Book on confirmation.** Steer the same browser task to the chosen slot.
   For the card hold use Stripe Link: call `wallet.list_payment_methods`
   with provider `stripe-link`, pick the current card, and pass
   `wallet_payment` with its `payment_method_id` on `browser.steer_task`.
   Boulevard may pre-select a merchant-saved card at checkout — the steer
   is what overrides it; naming Stripe Link in prose is not enough, the
   task needs the actual payment method passed on the steer call. The hold
   is the service price from `config.md`, charged after the appointment —
   verify that in the final review before submitting.
6. **Report.** Date/time, barber, shop, price, hold method, the
   cancellation policy, surcharge, and arrival notes from `config.md`,
   and that a confirmation email went to his address.

## Operating rules

- Booking implies agreement to reminder texts/emails — expected, no need to
  mention.
- If Fellow Barber changes their booking platform or flow, update `config.md`
  and this workflow.

## Dependencies
- haircut-signin (SKILL.md) — the Boulevard sign-in flow step 3 runs
- google_calendar (external skill) — freebusy query on the target window
- wallet (external provider) — card hold via wallet_payment on browser.steer_task
- browser (external tool) — availability check and booking on the Boulevard site
- record-learning (bin/record-learning) — learning loop

## Learning loop

Owned by the record-learning skill (see Dependencies). Record with
`~/workspace/custom-skills/record-learning/bin/record-learning haircut-book "<learning>"`.
