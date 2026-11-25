---
name: "inventory"
description: "Track the shared Inventory list"
---

# Inventory

The shared model for Peter's Inventory list (a Google Tasks list):
the household's running "we're low / we need" notebook. Domain
suites (hh-kitchen, camera-batteries) feed off this one list
through this skill; none of them talks to Google Tasks directly.

`bin/inventory` reads the list and completes items on it:

- `bin/inventory list` — the open items, title and notes.
- `bin/inventory complete "<title>"` — mark one item complete,
  by exact title, verified after the write.

## The completion rule

An item is completed only when its need is actually fulfilled —
never when it is merely ordered, carted, or planned. What counts
as fulfilled is the calling domain's call: for kitchen goods,
delivered (hh-kitchen-reconcile); for a battery order, the order
actually submitted (camera-batteries-order). The domain skill
verifies fulfillment first, then calls `complete`. This skill
owns the write; the domain owns the judgment.

## Routing

This skill does not classify items. The gather skills read the
list through `bin/inventory list` and route each item to their
domain by their own rules (hh-kitchen-restock's grocery judging,
camera-batteries' device matching). An item no domain claims
stays open and is presented as-is.

## Dependencies
- google_tasks (external, /opt/hatch/bin/hatch_gws_cli) — the Inventory list, read and completed through bin/inventory; never reimplement its auth
- record-learning (bin/record-learning) — learning loop

## Learning loop

Owned by the record-learning skill (see Dependencies). Record with
`~/workspace/custom-skills/record-learning/bin/record-learning inventory "<learning>"`.
