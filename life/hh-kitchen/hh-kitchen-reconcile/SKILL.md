---
name: "hh-kitchen-reconcile"
description: "Reconcile a delivered HH Kitchen restock"
---

# HH Kitchen Reconcile

Runs after an HH Kitchen order is delivered.

## Reconcile

1. Read the order record from the local config
   (`~/workspace/custom-skills/hh-kitchen-restock/bin/restock list`)
   and the delivery outcome from the platform's order record: what
   arrived as ordered, what was substituted, and what was not
   found or refunded.
2. An Inventory item counts as filled when it was delivered as
   ordered, or substituted and Peter kept the substitution. For
   each filled Inventory item, run
   `~/workspace/custom-skills/inventory/bin/inventory complete "<Inventory title>"`
   with the task's exact title. Leave every unfilled item on the
   list for the next run; never complete a task from the order
   alone — delivery is the evidence.
3. Update the config with what the order taught: a substitution
   Peter kept becomes the item's recorded product, a new brand he
   approved becomes its recorded brand, written with
   `~/workspace/custom-skills/inventory/bin/inventory learn`.
   When it is unclear whether a substitution or brand should stick,
   ask Peter first and record only his answer.
4. Report what was marked off, what stays, and what was learned,
   naming any substitutions Peter has not already seen.

## Dependencies
- hh-kitchen-restock (bin/restock) — the order log and the preference write; never reimplement them
- inventory (bin/inventory) — completing Inventory items, after delivery is verified here, and the learn write for preferences
- ordering-platform (external, the platform named in the local config store.platform) — the order record that shows what was actually delivered
- record-learning (bin/record-learning) — learning loop

## Learning loop

Owned by the record-learning skill (see Dependencies). Record with
`~/workspace/custom-skills/record-learning/bin/record-learning hh-kitchen-reconcile "<learning>"`.
