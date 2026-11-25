---
name: "hh-kitchen-gather"
description: "Gather the HH Kitchen restock ask list"
---

# HH Kitchen Gather

Builds the ask list for an HH Kitchen restock and presents it to
Peter. A cron initiates this skill; Peter's answer is what starts
a cart, through the hh-kitchen-build skill. Gathering never
touches a cart and never places an order.

The staple list, the store, and the Inventory judgment rules live
in the hh-kitchen-restock skill; this skill defers to its
`bin/restock` CLI for all of them.

## Gather

1. Run `~/workspace/custom-skills/hh-kitchen-restock/bin/restock inventory`
   for the open Inventory items, and keep the grocery-store-like
   ones, judging by the hh-kitchen-restock rules. The Inventory
   list is primary.
2. Run `~/workspace/custom-skills/hh-kitchen-restock/bin/restock list`
   for the staples and learned items.
3. Present one ask list, Inventory items first, then the staples
   as a checklist (checkboxes when the surface offers them, a
   plain numbered list otherwise). Every staple defaults to ask:
   nothing is a yes until Peter checks it.
4. Stop there. Peter's reply, with what he checked, is the trigger
   for hh-kitchen-build.

## Dependencies
- hh-kitchen-restock (bin/restock) — the config, the staples, and the Inventory read; never reimplement them
- record-learning (bin/record-learning) — learning loop

## Learning loop

Owned by the record-learning skill (see Dependencies). Record with
`~/workspace/custom-skills/record-learning/bin/record-learning hh-kitchen-gather "<learning>"`.
