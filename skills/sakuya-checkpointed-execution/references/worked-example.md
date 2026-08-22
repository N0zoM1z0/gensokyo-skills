# Worked example: add a required column without downtime

## Input

> Add a non-null `region` column to a 100-million-row customer table without downtime. Produce the runbook only.

## State model

- Current: writers know no `region` field; all rows are valid under the old schema.
- Target: every row has a valid region and all writers require it.
- Invariants: reads and writes remain available; mixed-version application instances remain compatible.
- Abort condition: error budget burn, replication lag above the agreed threshold, or unclassified rows above the allowed count.

## Checkpointed runbook

1. Add the nullable column. Verify old and new application versions can read the schema.
2. Deploy dual-compatible code that writes `region` when known and reads a fallback when absent. Verify real writes through the external API.
3. Backfill in bounded batches. At every batch checkpoint, record row range, lag, error rate, and unmatched count.
4. Stop new null creation and verify a full operating interval with zero new nulls.
5. Gate the constraint change on a fresh zero-null query, healthy lag, tested restoration plan, and named approval.
6. Add the non-null constraint using the database's safe validation path.
7. Remove fallback behavior only after every supported writer version has left the fleet.

## Recovery matrix

- Adding the nullable column: reversible after compatibility confirmation, but dropping it would destroy any newly written values.
- Dual-compatible code: reversible while the old schema remains accepted.
- Backfill: compensatable, not rollback; previous unknown values cannot be recreated by deleting the new values.
- Enforcing non-null: reversible only if the database supports dropping the constraint within the window; write behavior still requires coordination.
- Removing fallback: operationally irreversible for old writers once compatibility scaffolding disappears.

## Go/no-go gate

Proceed to constraint enforcement only with fresh evidence for zero nulls, acceptable lag, healthy error budget, operator approval, and a tested route to remove the constraint or roll forward.

## Final verification

Create and update a customer through the external API, read it through every supported client path, verify no nulls and no lag regression after one operating interval, then assign an owner and date for compatibility cleanup.

## Why this is Sakuya-shaped

The plan treats every step as a timed state transition, stops before irreversible impact, and refuses the fantasy that reversing a command necessarily restores the former world.
