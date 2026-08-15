# Worked example: a queue for one nightly report

## Input

> We plan to add Kafka, Redis, a worker fleet, and a scheduler so one internal report can run nightly from a 200 MB database table.

## Frozen outcome

Produce one recoverable report by 07:00 each day. Real constraints: do not overlap runs, keep seven days of results, and alert on failure. Real-time processing and horizontal scale are non-goals.

## Moving-part inventory

Scheduler, broker, cache, producers, consumers, worker deployment, result store, monitoring, and schemas can fail or change independently.

## Three-part baseline

1. Existing system scheduler.
2. One idempotent report command with a lock.
3. Existing object storage plus monitoring.

## First real constraint

If measured runtime exceeds the overnight window, a single process fails the deadline. Until measurement shows that, a worker fleet solves a forecast rather than a constraint.

## Earned complexity

Add partitioned workers only if runtime measurement proves the deadline failure. A broker remains unearned unless independent producers or delivery durability becomes a requirement.

## Why this is Cirno-shaped

The answer is aggressively small, but it still accounts for locking, recovery, retention, and alerting. It permits complexity to return when evidence defeats the simple plan.
