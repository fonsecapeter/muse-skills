---
name: "hh-kitchen-build"
description: "Build an HH Kitchen restock cart from Peter's gather answer"
---

# HH Kitchen Build

Turns Peter's answer to an hh-kitchen-gather ask into a built
cart at the configured store, on the configured platform. His response is the
trigger: no answer, no cart. Building never submits an order;
that is hh-kitchen-submit's job, after its own confirmation.

The config, the shorthands, and the learned products live in the
hh-kitchen-restock skill; this skill defers to its `bin/restock`
CLI for all of them.

## Build

1. Take the items Peter checked in his gather reply. Resolve every
   shorthand with `~/workspace/custom-skills/hh-kitchen-restock/bin/restock resolve`
   before searching, and use each entry's learned product and brand.
2. Build the cart at the store and on the platform named in the
   local config, following that platform's connector doc for
   search, cart, and presentation. Verify the retailer matches
   the configured store before adding anything.
3. Show Peter the built cart and stop. Submitting belongs to
   hh-kitchen-submit, which confirms with him first.

## Dependencies
- hh-kitchen-restock (bin/restock) — the config and shorthand resolution; never reimplement them
- ordering-platform (external, the platform named in the local config store.platform; currently instacart at /opt/hatch/bin/instacart) — store search and cart; its connector doc governs its use
- groceries (external skill, /opt/muse/skills/groceries/SKILL.md) — basket and presentation rules this skill follows
- record-learning (bin/record-learning) — learning loop

## Learning loop

Owned by the record-learning skill (see Dependencies). Record with
`~/workspace/custom-skills/record-learning/bin/record-learning hh-kitchen-build "<learning>"`.
