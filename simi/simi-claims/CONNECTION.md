# simi-claims — CONNECTION

How this skill connects to Peter's systems.

## Gmail, Google Drive, Google Sheets

All three go through the vendored Google Workspace CLI (`hatch_gws_cli`),
same as the other skills. No separate credentials to manage. Each of
`hatch_gws_cli gmail|drive|sheets status` must read `connected`.

If any comes back not connected, follow that skill's SKILL.md connect flow
(post the connect link, wait for Peter).

## Nationwide (my.petinsurance.com)

Peter files manually: the portal bot-checks the Muse browser, so
there is no browser filing flow. Tony's part is staging the invoice
and handing him the PDF and the login link. Never store or reuse his
Nationwide credentials.

## Learning loop

Owned by the record-learning skill (see Dependencies). Record with
`~/workspace/custom-skills/record-learning/bin/record-learning simi-claims "<learning>"`.
