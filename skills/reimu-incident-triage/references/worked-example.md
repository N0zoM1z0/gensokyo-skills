# Worked example: intermittent CI failures

## Input

> CI became flaky after splitting one test job into four. Some failures mention the database, some time out, and one team wants to rewrite the test harness.

## Actual incident

After the test job was parallelized, tests sharing the same database namespace intermittently observe each other's state instead of isolated fixtures when workers overlap.

## Signal ledger

- Evidence: failures begin after parallelization; colliding tests share namespace identifiers.
- Consequences: timeouts and inconsistent assertions.
- Context: the serial job remains stable.
- Noise: a broad test-harness rewrite has no evidence yet.
- Unknown: whether cleanup races or name collisions are primary.

## Smallest discriminating observation

Run two failing test groups concurrently with unique namespace logging. Compare cleanup timestamps and namespace IDs.

## Smallest safe action

Assign a unique namespace per worker as reversible containment. Keep the serial fallback as rollback.

## Verification

Run the original parallel job repeatedly with collision detection enabled. Treat a clean run as recovery evidence, not proof that no other test-isolation defect exists.

## Why this is Reimu-shaped

The workflow rejects the proposed rewrite, isolates one abnormal transition, restores normal behavior narrowly, and leaves structural follow-up explicit.
