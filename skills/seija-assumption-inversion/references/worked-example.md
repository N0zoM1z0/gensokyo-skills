# Worked example: centralize every customer's data

## Default argument

> We must copy every customer's raw data into one warehouse because analytics needs one place to query, otherwise cross-customer reporting is impossible.

## Assumption ledger

- Fact: reports need comparable aggregates.
- Preference: analysts want one query surface.
- Assumption: comparable results require centralized raw data.
- Forecast: federated queries will be too slow and difficult.

## Single inversion

Move computation to governed customer stores and centralize only schema-aligned aggregates. Preserve the reporting outcome, access control, and audit requirements.

## Strongest counterexample

For three representative customers, run the same versioned aggregation locally, sign the result, and combine only aggregate rows. Measure correctness, latency, operational work, and privacy exposure against the warehouse pipeline.

## Dependency fallout

Raw-data ingestion, broad central access, deletion replication, and some warehouse storage collapse. Version distribution, aggregate verification, and partial-result handling become more important.

## Reconciled judgment

The original premise becomes `conditional`: central raw data is not inherently required, but the inverted design must prove acceptable latency and operational control.

## Why this is Seija-shaped

The workflow overturns the load-bearing premise rather than merely deleting components, then makes the inverted world earn adoption through a concrete test.
