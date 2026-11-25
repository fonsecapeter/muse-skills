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

## The item

Under the list sits one unified item catalog (the local config
in `config.json`), owned by this skill. Every purchasable thing
in every domain is the same core object — one model, with slight
variations by type, the way Studio 1Way projects are all
projects whether woodwork, ceramic, or painting:

- **id**: stable unique id, assigned once at creation and never
  changed. Everything else is an editable attribute; composites
  link by id, so edits never break a link.
- **name**, **shorthand** (the word Peter actually says),
  **aliases**: how the item is named and resolved.
  `bin/inventory resolve "<term>"` resolves a term to exactly
  one item, across all domains.
- **type**: the discriminator — `food`, `battery`, `household`,
  `other`, extended as domains appear.
- **product**, **brand**, **product_id**: the exact thing he
  likes, on a domain's platform. Empty is a valid state: an
  unspec'd item is picked fresh at order time, by preference.
- **default_quantity**, **action** (default `ask`), **notes**.

Type- and domain-specific fields live in namespaced blocks on
the same record, never in the core: a battery carries
`battery: {spec}`; kitchen membership is `kitchen: {group}`
(the line, backstock, specials, learned). A domain reads its
own block and ignores the rest.

Higher-level things are composites that reference items by id
and live in their domain's config: kitchen spec cards (meals),
camera devices (slots of {item id, quantity}). The catalog is
the bottom of the model; composites never duplicate item data.

`bin/inventory items` prints the catalog. `bin/inventory learn
"<name>"` creates or updates an item — the write path for
preferences a domain learns (a brand Peter names, a product
that worked) — with `--type` and `--kitchen-group` when the
item is new.

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
