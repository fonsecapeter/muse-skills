---
name: "hh-kitchen-restock"
description: "Restock kitchen staples from the configured store"
---

# HH Kitchen Restock

The shared model for the HH Kitchen restock suite. The content
lives in the local config named in `config.json` (outside this
repo): the store, the staple list with the brands and shorthands
Peter uses, and what has been learned about Inventory items.
`bin/restock` reads and writes that local config; it never
touches a cart. The Inventory list itself belongs to the
inventory skill. 

## The local config

The config holds what is kitchen-only: the **store** (name,
retailer_name, platform, note — no skill in this suite names a
store or a platform; both come from here), **preferences**,
**spec cards**, and the **orders** log. The items themselves
live in the inventory skill's unified catalog; an item belongs
to the kitchen when it carries a `kitchen` block, whose `group`
is its shelf, by churn, named the way a kitchen names them:
**the line** — the front line, high churn, the regular store
run; **backstock** — keeps a long while, rarely needed;
**specials** — one-offs for a dish or hosting; **learned** —
grocery-like items seeded from the Inventory list that belong
to no group yet.

Item fields are the inventory skill's item model (id, name,
shorthand, product, brand, product_id, default_quantity,
action); this suite defers to it. An item's id never changes,
so spec cards link by id and survive any brand or size edit.

**Spec cards** are the meals, as named sets Peter can order
whole or by missing pieces; a spec card's items list entry ids,
or another spec card's id, across groups.

## The suite

This skill owns the shared model: the local config, the entry
fields above, and `bin/restock`. The four phases of a restock are
their own skills, and each defers to this one for the config:

- **hh-kitchen-gather** builds and presents the ask list.
- **hh-kitchen-build** builds the cart from Peter's gather answer.
- **hh-kitchen-submit** submits a built cart and records the
  order info.
- **hh-kitchen-reconcile** closes out a delivered order against
  the Inventory list and this config.

Judging Inventory items, shared by all four: grocery-store-like
means food, drink, and household consumables a grocery store
stocks. Respect an item's notes (a note naming another store wins).
Skip gear, medication, and anything the notes route elsewhere.

When an Inventory item is new or its product is unlearned, ask
Peter which product he gets; after he answers, record it next to
that item with `bin/inventory learn` so the next run already knows.

## Dependencies
- ordering-platform (external, the platform named in the local config store.platform) — store search and cart; its connector doc governs its use
- inventory (bin/inventory) — the Inventory list itself: reading it and completing items on it
- record-learning (bin/record-learning) — learning loop

## Learning loop

Owned by the record-learning skill (see Dependencies). Record with
`~/workspace/custom-skills/record-learning/bin/record-learning hh-kitchen-restock "<learning>"`.
