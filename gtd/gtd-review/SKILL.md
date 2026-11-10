

# GTD Review

Open counts for Google Tasks Intake and Inventory plus the Notion
TODO database, with links so Peter can process Intake himself. The
system map lives in `gtd/SYSTEM.md`; Peter does the processing
himself.

## Steps

1. **Collect the counts.** Run `bin/gtd-counts` in this skill's directory. It
   reads its values from `config.md` and prints JSON like
   `{"intake": 12, "inventory": 3, "notion_todo": 41}`. A `null` value means
   that source was unreachable — report it as unavailable and continue with
   the rest.
   - For anything Notion, `bin/gtd-counts` calls the `bin/notion-api`
     CLI named in `config.md` instead of reimplementing auth.
   - If the Tasks API is rate-limited (HTTP 429), re-run with
     `--skip-google-tasks` so the digest still goes out with the Notion count.
2. **Deliver the digest in chat.** Peter has ADHD and dyslexia: bullets, white
   space, short. No walls of text, no full task lists. Roughly eight
   lines or fewer:
   - One bullet per Google Tasks list: Intake with its open count, Inventory
     framed as items "to restock" (e.g. "- Inventory: 5 to restock").
   - One bullet: Notion TODO open count.
   - One line: link labeled "Open Google Tasks" (https://tasks.google.com/)
     so Peter can go see the items himself.
   - A blank line, then one line: link labeled "TODO database" to the Notion
     TODO actions view (in `config.md`).
   - One short nudge: process Intake — clarify each item (do it, file it into
     a Notion project, or delete it).

## Rules

- Read-only.
- Plain language only. No command names, no IDs, no raw JSON in the reply.

## Dependencies
- notion (bin/notion-api) — reads the TODO database via bin/gtd-counts; never reimplement auth
- record-learning (bin/record-learning) — learning loop

## Learning loop

Owned by the record-learning skill (see Dependencies). Record with
`~/workspace/custom-skills/record-learning/bin/record-learning gtd-review "<learning>"`.
