---
name: "camera-batteries"
description: "Track which device takes which batteries"
---

# Camera Batteries

The shared model for the camera-batteries suite. Devices live
in the local registry named in `config.json` (outside this
repo); the batteries themselves are items in the inventory
skill's unified catalog (type `battery`, spec in the item's
`battery` block), read through its CLI. `bin/batteries` joins
the two; it never orders anything.

## The registry

Devices only — a composite over catalog items, many-to-many
with quantity on the join: a device takes one or more battery
items, and a battery item can serve several devices.

- A **device**: id, name ("Canon AE-1"), aliases ("ae-1"), and
  slots — a list of {battery_id, quantity}, where battery_id is
  a catalog item id. Quantity lives on the slot: the Instax
  takes 2× CR2, the AE-1 takes 1× PX28.

Every id is assigned once and never changes; quantity is an
editable attribute. Not every device is a camera — anything
battery-powered that Peter wants resolved the same way
(the Jeep's AirTag) registers as a device.

## Resolving

`bin/batteries resolve "<text>"` matches the devices a text
names — an Inventory item like "canon ae-1 batteries", or Peter
asking directly — and returns each device with its slots
resolved to full battery specs: what to order, and how many.
The device decides the battery, never the text: an item that
names the wrong battery for a device resolves to the battery
the registry says the device takes.

## Dependencies
- inventory (bin/inventory) — the shared Inventory list this suite feeds off
- record-learning (bin/record-learning) — learning loop

## Learning loop

Owned by the record-learning skill (see Dependencies). Record with
`~/workspace/custom-skills/record-learning/bin/record-learning camera-batteries "<learning>"`.
