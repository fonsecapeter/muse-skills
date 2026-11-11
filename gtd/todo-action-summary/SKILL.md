

# Todo Action Summary

Two halves: the full open list, then your judgment on top of it.
Read-only.

## Steps

1. **The list.** Run `bin/todo-summary` in this skill's directory.
   It reads its values from `config.md` and prints JSON with every open todo:
   `title`, `project`, `priority`, `due`, `created`, `days_overdue`, sorted
   P1-first. If `notion_ok` is false, say the check couldn't reach Notion and
   stop.
   - For anything Notion, `bin/todo-summary` calls the `bin/notion-api`
     CLI named in `config.md` instead of reimplementing auth.
2. **Present the list.** Peter has ADHD and dyslexia: bullets, white space,
   short. Group by project, one tight line per todo: title plus priority
   and/or due where set. This is the full picture — keep each line short,
   no essays.
3. **Attention flags (agentic).** Now apply judgment: call out the 2–4 items
   that aren't getting the attention they should. Signals worth weighing:
   overdue items; P1s with no due date; high-stakes items (Neha, travel
   documents, money, security) sitting idle; items created 30+ days ago
   untouched (`stale_days` in `config.md`); important-looking todos with no
   priority set. One line per flag saying why it matters. Cap it at four —
   a nudge, not a lecture.
4. **Link.** End with the Notion TODO actions view link from `config.md`
   so Peter can jump straight in.

## Rules

- Read-only.
- Plain language only. No command names, no IDs, no raw JSON in the reply.
- Due dates are real commitments in Peter's system, not loose plans. Never
  suggest adding a due date casually — only when he'd actually honor it.

## Dependencies
- notion (bin/notion-api) — reads the TODO database via bin/todo-summary; never reimplement auth
- record-learning (bin/record-learning) — learning loop

## Learning loop

Owned by the record-learning skill (see Dependencies). Record with
`~/workspace/custom-skills/record-learning/bin/record-learning todo-action-summary "<learning>"`.
