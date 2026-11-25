---
name: "hh-kitchen-submit"
description: "Submit a built HH Kitchen restock order"
---

# HH Kitchen Submit

Submits a cart built by hh-kitchen-build. A gather answer or a
built cart is not a confirmation to submit; the confirmation
happens in this step.

## Submit

1. Show Peter the final cart, its total, and the delivery window.
2. Wait for his explicit confirmation to submit. Without it, stop
   with the cart intact.
3. Place the order, following the configured platform's
   connector doc checkout flow.
4. Record the order info (order id, what was ordered, the delivery
   window, and which items came from the Inventory list) with
   `~/workspace/custom-skills/hh-kitchen-restock/bin/restock log-order "<summary>"`.

## Dependencies
- hh-kitchen-restock (bin/restock) — the order log; never reimplement it
- ordering-platform (external, the platform named in the local config store.platform) — checkout; its connector doc governs its use
- record-learning (bin/record-learning) — learning loop

## Learning loop

Owned by the record-learning skill (see Dependencies). Record with
`~/workspace/custom-skills/record-learning/bin/record-learning hh-kitchen-submit "<learning>"`.
