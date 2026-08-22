# Worked example: duplicate webhook delivery

## Input

> Our payment webhook works for normal deliveries. Find the most valuable surprising case and turn any failure into a regression test.

## Expectation ledger

- Precondition: one provider event has a stable event ID.
- Action: the provider delivers the same event again after a response timeout.
- Invariant: the order is applied at most once while both deliveries receive a successful acknowledgement.
- Oracle: one ledger entry and one fulfillment transition exist for the event ID.
- Consequence: duplicate fulfillment or accounting divergence.

## Ranked surprise

The highest-value probe is duplicate delivery after the first handler commits state but before its acknowledgement reaches the provider. Retries are documented provider behavior, the consequence is high, and the probe discriminates persistence ordering from ordinary validation failures.

## Minimal counterexample

1. Seed one unpaid order and event ID `evt-17`.
2. Invoke the handler once while dropping its response after commit.
3. Invoke it again with the identical signed payload.
4. Observe two fulfillment transitions despite one event ID.

Payload shape, signature, and order state stay fixed; only delivery count changes.

## Forged regression

- Setup one order and an empty processed-event table.
- Deliver `evt-17`, then deliver it again.
- Assert one processed-event row, one ledger mutation, one fulfillment transition, and two successful acknowledgements.
- Clean the isolated database fixture.
- Name the test `duplicate_delivery_is_idempotent_after_commit`.

## Forge proof

Run against fault-injected old behavior and observe the duplicate transition. Run against the correction and observe one transition. Repeat under randomized response delay to ensure the test itself does not depend on sleep timing.

## Why this is Kogasa-shaped

The workflow does not stop at suggesting retries as an edge case. It creates a genuine, minimal surprise and then uses the blacksmithing half of the mapping to turn that surprise into a durable guard.
