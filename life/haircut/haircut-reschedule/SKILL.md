# Haircut Reschedule

Move Peter's Fellow Barber appointment to a new slot.

- Open the appointment from the confirmation email's blvd.app token
  link. haircut-signin covers the portal's code round — Peter enters
  that code himself via browser takeover.
- In the portal, choose **Modify appointment → Reschedule** and pick
  the new slot. The appointment moves directly; no cancel/rebook.
- Report the new date/time, and that a fresh confirmation email went
  to his address.

## Dependencies
- haircut-signin (SKILL.md) — opening the appointment in the portal
- browser (external tool) — the reschedule on the Boulevard portal
- record-learning (bin/record-learning) — learning loop

## Learning loop

Owned by the record-learning skill (see Dependencies). Record with
`~/workspace/custom-skills/record-learning/bin/record-learning haircut-reschedule "<learning>"`.
