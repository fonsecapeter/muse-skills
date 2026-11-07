# simi-claims — CONNECTION

How this skill connects to Peter's systems.

## Gmail, Google Drive, Google Sheets

All three go through the vendored Google Workspace CLI (`hatch_gws_cli`),
same as the other skills. No separate credentials to manage.

- `hatch_gws_cli gmail status` — must be `connected` (verified 2026-10-08).
- `hatch_gws_cli drive status` — must be `connected` (verified 2026-10-08).
- `hatch_gws_cli sheets status` — must be `connected` (verified 2026-10-08).

If any comes back not connected, follow that skill's SKILL.md connect flow
(post the connect link, wait for Peter) — never invent a URL or ask for
credentials.

## Nationwide (my.petinsurance.com)

Peter files manually — he is in the loop for every Nationwide step.
The portal blocks automated browsers outright (Akamai challenge;
sign-in sessions don't persist), so there is no browser flow to offer
or drive, and this dates from before that was known — don't resurrect
it. Tony's part: stage the invoice, hand Peter the PDF and the login
link, and log what he files from the claim-details screenshot he
sends back. Never store or reuse his Nationwide credentials.

## Learning loop

Owned by the record-learning skill (see Dependencies). Record with
`~/workspace/custom-skills/record-learning/bin/record-learning simi-claims "<learning>"`.
