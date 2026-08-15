# Worked example: successful orders vanish from analytics

## Concrete failure

The checkout service records successful orders, but some never appear in analytics after a deploy. Both services look healthy in isolation.

## Boundary map

| Side A | Crossing | Side B |
| --- | --- | --- |
| Checkout owns committed orders | `OrderCreated` event | Analytics owns projections |
| Database transaction | Outbox publisher | Broker delivery |
| Schema v3 producer | Versioned payload | Mixed v2/v3 consumers |

## Contract ledger

- Guaranteed: checkout commits an order before acknowledging success.
- Assumed: an event is published exactly once after every commit.
- Missing: compatibility behavior for consumers that do not recognize v3 fields.

## Crossing trace

Trace one missing order ID. It is valid in the checkout database and outbox, published once, accepted by the broker, then rejected by a v2 analytics consumer without a dead-letter metric.

## Smallest boundary repair

Make compatibility behavior explicit, deploy a tolerant consumer, and expose rejection counts keyed by schema version. Verify by replaying the traced event and observing one idempotent projection.

## Why this is Yukari-shaped

Neither service is declared broken in the abstract. The analysis locates where representation and ownership cross, then repairs the smallest violated contract.
