---
name: yukari-boundary-analysis
description: Diagnose systems by mapping interfaces, ownership, trust zones, lifecycle transitions, and edge conditions, then trace failures across the most suspicious boundary. Use for integration bugs, distributed systems, API mismatches, unclear responsibility, state transitions, migrations, or failures that appear only between otherwise working components. Do not use for a clearly local bug or generic architecture brainstorming without a concrete crossing to inspect.
---

# Yukari Boundary Analysis

Treat the character framing as a mnemonic for a working method. Do not role-play unless the user asks.

## Objective

Find where a valid thing on one side becomes invalid, ambiguous, unowned, or unobservable on the other.

## Operating bias

- Treat interfaces and transitions as first-class system components.
- Inspect ownership, trust, time, representation, and lifecycle boundaries.
- Follow one concrete request, record, user, or event end to end.
- Repair the contract before redesigning the whole landscape.

## Required context

Collect:

- the observed failure or decision that motivates the analysis;
- participating components, people, stores, or states;
- data or control flow between them;
- owners and trust zones;
- timing, retries, versions, and lifecycle stages;
- the last point where the traced thing is known to be valid.

When no concrete failure exists, ask for a scenario or select one representative crossing and label it as hypothetical.

## Procedure

### Gap Sign — Name both sides

For each candidate boundary, name:

- producer and consumer;
- upstream and downstream owner;
- source and destination representation;
- source and destination trust zone;
- state before and state after the crossing.

If either side cannot be named, flag an ownership or modeling gap.

### Border Sign — Write the contract

Record the boundary contract:

- accepted inputs and emitted outputs;
- invariants and validation;
- authority and responsibility;
- error, timeout, retry, and cancellation behavior;
- compatibility and version assumptions;
- observability available on both sides.

Separate documented guarantees from behavior inferred by accident.

### Crossing Sign — Follow one traveler

Trace one concrete request, event, file, token, or state transition. At every crossing, record its identity, representation, timestamp, owner, and validation result.

Mark the last valid point and the first invalid or ambiguous point. Prefer trace evidence over architecture diagrams that describe intent.

### Threshold Sign — Test the edges

Test relevant edge conditions:

- missing, empty, duplicate, delayed, or out-of-order input;
- retry after partial success;
- timeout, cancellation, and restart;
- schema or version skew;
- serialization, locale, timezone, and precision changes;
- permission or trust-zone transitions;
- creation, migration, expiration, and deletion;
- network, process, storage, or human handoff failure.

Choose cases that can distinguish competing boundary failures; do not enumerate mechanically.

### Boundary Repair — Change the smallest contract

Choose one repair class:

- clarify the contract;
- validate earlier or later;
- move ownership;
- add idempotency, buffering, or compatibility handling;
- improve cross-boundary observability;
- merge an artificial boundary;
- split a dangerous shared boundary.

State the new invariant and how both sides will verify it.

## Characteristic failure mode

This method can become abstract and find boundaries everywhere.

Before recommending a change, perform one concrete-failure check:

- Which observed failure does this boundary explain?
- What trace or test would falsify the explanation?
- Could the bug live entirely on one side?
- Is the proposed boundary change cheaper than a local fix?

If the abnormality is clearly local, hand off to incident triage. If the boundary is real but the design is bloated, hand off to radical simplification.

## Output contract

Return:

1. **Concrete failure** — the motivating observation.
2. **Boundary map** — two sides, owners, representations, and trust zones.
3. **Contract ledger** — guaranteed, assumed, and missing behavior.
4. **Crossing trace** — last valid and first invalid point.
5. **Edge tests** — prioritized discriminating cases.
6. **Smallest boundary repair** — changed invariant, verification, and new risk.

## References

Read [references/provenance.md](references/provenance.md) only when explaining the character-to-workflow mapping or reviewing fanwork provenance. Read [references/worked-example.md](references/worked-example.md) when the analysis is drifting away from a concrete crossing.
