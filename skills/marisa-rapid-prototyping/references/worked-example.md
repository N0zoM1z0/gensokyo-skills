# Worked example: can SQLite replace a service for this tool?

## Decision at stake

Choose whether a single-user desktop tool needs a local SQLite store or a separate database service.

## Risky assumption

If SQLite supports the tool's concurrent import and search workload, then a representative import can run while search latency remains below the user-visible threshold without lock failures.

## Borrowed parts

- Reuse the application's existing repository interface.
- Use official SQLite behavior and the current data model.
- Avoid building a new UI, sync layer, or migration system for the spike.

## Smallest experiment

Load a representative dataset, start one import writer, run the real search query mix, and record latency and lock errors. Use a temporary database and a fixed timebox.

## Decision

- Proceed if latency and locking stay inside the threshold.
- Modify journal or transaction configuration if results identify a narrow bottleneck.
- Stop if the actual concurrency model requires unsupported multi-host writes.

## Prototype debt

The spike does not establish backup, schema migration, corruption recovery, or production packaging. Adoption requires those gates separately.

## Why this is Marisa-shaped

The workflow borrows the existing interface, builds only the dangerous path, runs it early, and refuses to turn a successful demo directly into a production claim.
