---
name: "camera-batteries"
description: "Track which device takes which batteries"
---

# Camera Batteries

The shared model for the camera-batteries suite. The content
lives in the local registry named in `config.json` (outside this
repo): the devices Peter owns and the batteries each one takes.
`bin/batteries` reads that registry; it never orders anything.

## The registry

Two catalogs, many-to-many, with quantity on the join — a
device takes one or more battery types, and a battery type can
serve several devices:

- A **battery**: id, type ("CR2"), spec ("3V lithium"), preferred
  brand, notes.
- A **device**: id, name ("Canon AE-1"), aliases ("ae-1"), and
  slots — a list of {battery_id, quantity}. Quantity lives on
  the slot: the Instax takes 2× CR2, the AE-1 takes 1× PX28.

Every id is assigned once and never changes; type, brand, and
quantity are editable attributes. Not every device is a camera —
anything battery-powered that Peter wants resolved the same way
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
