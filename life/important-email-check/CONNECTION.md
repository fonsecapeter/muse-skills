# Connection — important-email-check

Gmail is the built-in gmail skill's connector (external). This skill
reaches it only through `hatch_gws_cli gmail ...` (raw API form:
`users messages list/get`), the same pattern as simi-inbox-scan.

- No credentials live in this skill. If `hatch_gws_cli gmail` reports
  the account is not connected, the scan fails loudly and the run
  reports that Gmail couldn't be reached — reconnecting is done through
  the gmail skill's own connect flow, never from here.
- Read-only usage only: `messages.list` + `messages.get`. This skill
  never sends, modifies, labels, or deletes mail.
