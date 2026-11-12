# Email as Peter

How Peter writes email. Applies to any draft Tony writes for Peter to
send, and to mail Tony sends as him. Draft and send mechanics live in
the email-management skill (see Dependencies). This skill is the voice.

## Voice

- Plain and direct, first person. Write the way Peter talks.
- Use contractions.
- Short sentences, one idea each.
- Cut institutional phrasing. "Dear Visa Office", "I am writing to
  inquire", "Could you please advise", and "Thank you for any update
  you can share" all read as someone else.

## Open

- Greet with "Hello,".
- State the situation in a sentence or two, in plain words.
- Put the ask as its own short question: "Will it be ready in time?"
  "Is there anything else you need from us?"

## People, dates, numbers

- People go by first name: Neha, not "my wife". Peter and Neha
  together are "we".
- Dates read the way people say them: "next week (November 20)", not
  "Friday, November 20, 2026".
- Reference numbers stay exact. The words around them stay casual:
  "application no." plus the number, nothing grander.

## Details

- Facts go in a short bullet list under a plain lead-in: "For some
  more info:".
- One fact per bullet, in the order the reader needs them.
- No prose paragraph doing a list's job.

## Subject and close

- The subject says the thing, short: "Status of visa application"
  plus the number. No category label up front ("Status
  inquiry — ...").
- Close warm and brief: "Thanks in advance for any help!"
- Sign off "-- Peter". First name only.

## Dependencies

- email-management (external, /opt/muse/skills/email-management/SKILL.md) — draft and send mechanics; this skill is the voice on top
- record-learning (bin/record-learning) — learning loop

## Learning loop

Owned by the record-learning skill (see Dependencies). Record with
`~/workspace/custom-skills/record-learning/bin/record-learning email-as-peter "<learning>"`.
