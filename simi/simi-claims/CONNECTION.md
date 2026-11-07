# simi-claims — CONNECTION

How this skill connects to Peter's systems.

## Gmail, Google Drive, Google Sheets

All three go through the vendored Google Workspace CLI (`hatch_gws_cli`),
same as the other skills. No separate credentials to manage. Each of
`hatch_gws_cli gmail|drive|sheets status` must read `connected`.

If any comes back not connected, follow that skill's SKILL.md connect flow
(post the connect link, wait for Peter) — never invent a URL or ask for
credentials.

## Nationwide (my.petinsurance.com)

Peter files manually — he is in the loop for every Nationwide step,
and there is no browser filing flow. The portal does not block
automated browsers outright: the account-access page loads cleanly
(checked 2026-11-07); the one observed automated sign-in (Oct 2026)
hit a bot check after login. Tony's part: stage the invoice, hand
Peter the PDF and the login link, and log what he files from the
claim-details screenshot he sends back. Never store or reuse his
Nationwide credentials.

## Learning loop

Owned by the record-learning skill (see Dependencies). Record with
`~/workspace/custom-skills/record-learning/bin/record-learning simi-claims "<learning>"`.
