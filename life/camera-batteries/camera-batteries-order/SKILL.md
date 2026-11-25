---
name: "camera-batteries-order"
description: "Order batteries for a resolved device"
---

# Camera Batteries Order

Order batteries for devices resolved by camera-batteries — from
an Inventory item routed here, or Peter asking directly. Where
to buy is deliberately not this skill's business: Peter names
the store or route at order time, and this skill hand-waves the
buying mechanics to that route.

## Order

1. Resolve the devices with
   `~/workspace/custom-skills/camera-batteries/bin/batteries resolve "<text>"`.
   Show Peter the order spec — device, battery type and spec,
   quantity, preferred brand — and confirm before ordering.
2. Submit the order by the route Peter names. Nothing is ordered
   before his confirmation in this step.
3. Once the order is actually submitted, close the loop: for
   each Inventory item this order covered, run
   `~/workspace/custom-skills/inventory/bin/inventory complete "<Inventory title>"`.
   Submitted is the fulfillment for an order (the inventory
   skill's completion rule); a cart, a draft, or a planned order
   completes nothing. If the order came from Peter asking
   directly, there is no Inventory item to complete.

## Dependencies
- camera-batteries (bin/batteries) — the registry and resolution; never reimplement it
- inventory (bin/inventory) — completing the Inventory items an order covers
- record-learning (bin/record-learning) — learning loop

## Learning loop

Owned by the record-learning skill (see Dependencies). Record with
`~/workspace/custom-skills/record-learning/bin/record-learning camera-batteries-order "<learning>"`.
