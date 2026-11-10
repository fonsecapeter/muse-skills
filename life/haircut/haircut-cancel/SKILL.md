# Haircut Cancel

Cancel Peter's Fellow Barber appointment — including strays.

- Open the appointment via the confirmation email's Manage
  appointment link. haircut-signin covers the portal's code round.
- Cancel in the portal, then report: what was cancelled, and the fee
  the cancellation policy in haircut-book's `config.md` puts on it.

## Stray or duplicate confirmations

Boulevard can email a confirmation for a slot Peter never booked.
If one arrives, verify the live booking status before heading out —
check via the Manage appointment link or a quick call to the shop.
If the stray appointment isn't on the books, confirm the real one is
still there; if it is on the books, cancel or move it deliberately
rather than ignoring it.

## Dependencies
- haircut-signin (SKILL.md) — opening the appointment in the portal
- haircut-book (config.md) — the cancellation policy
- browser (external tool) — the cancellation on the Boulevard portal
- record-learning (bin/record-learning) — learning loop

## Learning loop

Owned by the record-learning skill (see Dependencies). Record with
`~/workspace/custom-skills/record-learning/bin/record-learning haircut-cancel "<learning>"`.
