---
name: "hh-kitchen-restock"
description: "Restock kitchen staples from the configured store"
---

# HH Kitchen Restock

The shared model for the HH Kitchen restock suite. The content
lives in the local config named in `config.json` (outside this
repo): the store, the staple list with the brands and shorthands
Peter uses, and what has been learned about Inventory items.
`bin/restock` reads and writes that local config and reads the
Inventory list; it never touches a cart.

## The local config

Each entry, staple or learned, carries the same fields:

- **name**: the plain item name ("oat milk").
- **shorthand**: the word Peter actually says ("malk"). A shorthand
  resolves to exactly one entry; resolve it with `bin/restock
  resolve` before searching the store.
- **product**: the exact product he likes ("MALK Unsweetened Almond
  Malk"). Empty until learned.
- **brand**: the brand, when it matters separately from the product.
- **product_id**: the learned product's id on the configured
  platform. Empty until learned.
- **default_quantity**: how much a restock buys.
- **action**: what a run does without being told. Staples default to
  `ask`: never added silently, always offered in case he forgot he
  needs them. `add` is set per entry only when Peter says so.

The config's **store** object names the store and how to reach it:
**name**, **retailer_name** (the store's name on the platform),
**platform** (the ordering platform's connector id), and a free
**note** (which location, and anything else worth knowing). No
skill in this suite names a store or a platform; both come from
here.

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
that item with `bin/restock learn` so the next run already knows.

## Dependencies
- ordering-platform (external, the platform named in the local config store.platform) — store search and cart; its connector doc governs its use
- google_tasks (external, /opt/hatch/bin/hatch_gws_cli) — the Inventory list, read through bin/restock; never reimplement its auth
- record-learning (bin/record-learning) — learning loop

## Learning loop

Owned by the record-learning skill (see Dependencies). Record with
`~/workspace/custom-skills/record-learning/bin/record-learning hh-kitchen-restock "<learning>"`.
