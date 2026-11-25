---
name: "inventory-gather"
description: "Gather the weekly Inventory ask across domains"
---

# Inventory Gather

The weekly front door for the Inventory list, and what the
Sunday cron invokes. One ask, routed: every open Inventory item
goes to the domain that owns it, and the kitchen's standing ask
(the line, backstock, specials) rides along. This skill builds
no cart and places no order; Peter's reply is the trigger for
each domain's own flow.

## Gather

1. Run `~/workspace/custom-skills/inventory/bin/inventory list`
   for the open Inventory items.
2. Route each item: grocery-store-like items (judged by the
   hh-kitchen-restock rules) belong to the kitchen; anything else
   is presented verbatim under "Also on Inventory".
3. Present one ask list: the routed Inventory items first, by
   domain, then the kitchen ask from hh-kitchen-gather (the line,
   backstock, specials as a checklist).
4. Stop there. Peter's reply routes onward: kitchen picks trigger
   hh-kitchen-build; other items are handled in chat or by their
   domain's flow when one exists.

## Dependencies
- inventory (bin/inventory) — the list itself; never reimplement it
- hh-kitchen-gather (SKILL.md) — the kitchen section of the ask
- hh-kitchen-restock (bin/restock) — resolving kitchen items against the config
- record-learning (bin/record-learning) — learning loop

## Learning loop

Owned by the record-learning skill (see Dependencies). Record with
`~/workspace/custom-skills/record-learning/bin/record-learning inventory-gather "<learning>"`.
