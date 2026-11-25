---
name: "hh-kitchen-gather"
description: "Gather the HH Kitchen restock ask list"
---

# HH Kitchen Gather

Builds the ask list for an HH Kitchen restock and presents it to
Peter. A cron initiates this skill. Gathering never touches a
cart and never places an order.

## Gather

1. Run `~/workspace/custom-skills/inventory/bin/inventory list`
   for the open Inventory items, and keep the grocery-store-like
   ones, judging by the hh-kitchen-restock rules.
2. Run `~/workspace/custom-skills/hh-kitchen-restock/bin/restock list`
   for the grouped items (the line, backstock, specials)
   and the learned items.
3. Present one ask list, Inventory items first, then the groups
   in order — the line, backstock, specials — as a checklist
   (checkboxes when the surface offers them, a plain numbered
   list otherwise).
4. Stop there. Peter's reply, with what he checked, is the trigger
   for hh-kitchen-build.

## Dependencies
- inventory (bin/inventory) — the Inventory list itself
- hh-kitchen-restock (bin/restock) — the config, the grouped items, and the Inventory read; never reimplement them
- record-learning (bin/record-learning) — learning loop

## Learning loop

Owned by the record-learning skill (see Dependencies). Record with
`~/workspace/custom-skills/record-learning/bin/record-learning hh-kitchen-gather "<learning>"`.
