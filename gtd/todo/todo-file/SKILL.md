---
name: "todo-file"
description: "File a new TODO"
---

# Todo File

Filing new todos into Peter's TODO database, his way. The notion
skill owns the API mechanics; all Notion access defers to its
`bin/notion-api`.

System map: `~/workspace/custom-skills/SYSTEM.md` — how Peter's
capture → todos → digests → completions system fits together.
Peter processes his Google Tasks Intake into Notion himself — never
move items between the two systems unless he explicitly asks.

## Check for an existing todo first

When Peter asks to save or file a todo, scan the open todos
(todo-find's `bin/find-todo`, several phrasings) before creating
anything. Scope is open todos (TODO / Doing / Parked); skip completed
ones unless there's a specific reason to expand. The one scan serves
three checks:

1. **Duplicate?** If a matching open todo exists, update it instead
   of creating a twin.
2. **Checklist child?** The match may be a *parent*, not the todo
   itself: if the new item sounds like it could live as an item in a
   found todo's body checklist, read that todo's body before deciding
   (only plausible parents — don't read every body). If it fits
   underneath, add it to that checklist and say so. (Model case,
   2026-10-14: the jury-duty item belonged under the address-update
   todo, not as its own todo.)
3. **Dependencies?** In the same pass, judge whether the new or
   existing todo is blocked by — or blocks — another open todo, and
   propose the link in the same breath, from the same scan.

## When creating

- **Title = the action to take.** Details go in the page body, only if
  needed. Logistics, dates, and account numbers stay out of titles.
- **No Priority** on new todos — Peter triages himself. **No Due date**
  unless it's a real commitment: for Peter a due date means "actually
  do it," never a loose plan.
- File under the matching **Project** when one clearly fits.
- **Dependencies** (Blocked by / Blocking): propose links in chat
  before adding them. Umbrella + step todos cross-link both ways when
  Peter asks for a set.

## Writing todo bodies

The body rules for the whole todo group — todo-update defers here
when it edits an existing body:

- **Keep it minimal.** Only what Peter needs to do the work — no
  background prose, no restating the title.
- **Separate reference from action.** Reference/info (specs, product
  names, measurements, links) goes in its own short section or lines,
  clearly apart from the actionable checklist — never mixed into
  checklist items or buried inside a step.
- **Checklist items are short and action-only.** One action per item,
  phrased as the action itself; no details, explanations, or
  sub-clauses packed into a step.
- **Order is execution order.** Verify the checklist is in the exact
  order Peter will perform the work before saving — a correct list in
  the wrong order is still wrong.

## Tooling

- Machine values (database IDs, the notion-api path) live in
  `config.md`.

## Dependencies
- notion (bin/notion-api) — all Notion reads/writes go through it; never reimplement auth
- todo-find (bin/find-todo) — the pre-creation scan for duplicates, parents, and dependencies
- record-learning (bin/record-learning) — learning loop

## Learning loop

Owned by the record-learning skill (see Dependencies). Record with
`~/workspace/custom-skills/record-learning/bin/record-learning todo-file "<learning>"`.
