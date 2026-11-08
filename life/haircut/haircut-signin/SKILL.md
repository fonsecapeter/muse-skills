# Haircut Sign-In

Signing in to Boulevard for Fellow Barber — the shared step for
haircut-book, haircut-reschedule, and haircut-cancel.

Boulevard signs in with an emailed code typed into **six separate
digit boxes**, on the booking widget and on the blvd.app client
portal alike. Gmail returns the code as a sealed reference, so the
digits come from Peter:

1. Enter Peter's email (kept in `~/USER.md`) on the sign-in screen to
   send the code. His standing permission covers the email entry
   (2026-10-01, haircut only).
2. Peter reads the 6 digits from the newest Fellow Barber code email
   in chat.
3. The browser task types them one by one into boxes 1→6 and submits.

Codes live 15 minutes, and requesting a new code replaces the
previous one — work from the newest code email.

The confirmation email's blvd.app token link opens an appointment
without the widget sign-in. The portal then sends its own code, and
Peter enters that one himself via browser takeover. The portal takes
a separate code round from the widget.

## Dependencies
- browser (external tool) — the Boulevard site where sign-in happens
- record-learning (bin/record-learning) — learning loop

## Learning loop

Owned by the record-learning skill (see Dependencies). Record with
`~/workspace/custom-skills/record-learning/bin/record-learning haircut-signin "<learning>"`.
