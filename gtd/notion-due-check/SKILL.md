# Notion Due Check

## Collect the due items

- Run `~/workspace/custom-skills/notion-due-check/bin/due-todos` to collect the items.

- Read the window and the link values from `config.md` in this skill's directory at run time.

- Read the JSON the script prints, which carries `overdue`, `due_today`, `due_soon`, `as_of` and `notion_ok`, with a `title`, `due` date and `project` on each item.

- Due dates come from the script; don't recompute them in prose.

- Filter out the closed statuses listed in `config.md` — completion is a `Status` select, not a Done checkbox.

- Adjust the due-soon window in `config.md` when the digest surfaces items too early or too late, rather than editing the script.

- Check the TODO database schema first if Notion queries start returning 400 errors.

- Stop and say the check could not reach Notion when `notion_ok` is false.

## Deliver the digest

- Group the items by timing under the headings Past stored date, Due today and Due soon, and never label an item overdue.

- Open the digest with one caveat line: stored dates are still being cleaned out, so a past date means worth a look rather than a missed commitment. Keep that framing until Peter confirms the audited due dates feel trustworthy.

- Give each todo one line with its title linked to its Notion page and its project named.

- Keep the digest short with bullets and white space, because Peter has ADHD and dyslexia.

- Send nothing user-visible when every list is empty, because the check ran clean and silence beats noise.

- End with the Notion TODO actions view link from `config.md` so Peter can jump straight in.

- Read-only. Plain language: no command names, no IDs, no raw JSON in the reply.

## Dependencies

- notion (bin/notion-api) — reads the TODO database via bin/due-todos; never reimplement auth

- record-learning (bin/record-learning) — learning loop

## Learning loop

Owned by the record-learning skill (see Dependencies). Record with
`~/workspace/custom-skills/record-learning/bin/record-learning notion-due-check "<learning>"`.
