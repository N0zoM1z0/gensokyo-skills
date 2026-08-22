# Worked example: SDK-breaking API rename

## Input

> Rename a public API field across the server, TypeScript SDK, Python SDK, docs, and tests. Three contributors can work in parallel, but the branch must remain mergeable.

## Whole-state contract

- Final deliverable: both SDKs and the server expose `account_id`; the old `user_id` remains accepted for one compatibility window.
- Invariants: wire format and deprecation behavior are identical across languages.
- Integrated acceptance: a consumer using either field completes the same end-to-end request, and generated documentation shows the transition.
- Central decision: the compatibility schema and removal date have one owner.

## Dependency map

The compatibility schema is interface-defining work and must land first. Server, SDK implementations, and documentation can then proceed independently. Generated fixtures are shared and remain owned by the schema packet.

## Work packets

### Packet A — compatibility contract

- Owned scope: API schema, generated fixture source, deprecation decision.
- Output: versioned schema plus old/new request fixtures.
- Evidence: schema validation and compatibility matrix.

### Packet B — server implementation

- Input: Packet A schema and fixtures.
- Owned scope: server parser and integration tests.
- Forbidden overlap: schema naming and SDK files.
- Evidence: old/new end-to-end requests produce identical domain state.

### Packet C — SDKs and docs

- Input: Packet A schema and fixtures.
- Owned scope: both SDK serializers, generated public docs, language-specific tests.
- Forbidden overlap: server behavior and schema source.
- Evidence: each SDK emits the canonical field and accepts the compatibility fixture.

## Gathering contract

Packet A owns interface conflicts. Packets B and C may report a schema problem but may not fork the contract. Every packet returns changed paths, checks run, and deviations from its frozen inputs.

## Merge sequence

Merge A, regenerate fixtures, validate B and C against the resulting revision, merge B, merge C, then run the consumer-level acceptance test across both SDKs.

## Merge-tax judgment

Keeping both SDKs together avoids duplicate edits to generated documentation and fixture adapters. Splitting them into two more packets would add coordination without an independent contract boundary.

## Why this is Suika-shaped

The workflow begins with one dense whole, makes only earned parts sparse, binds them with direct promises, and refuses to call the task complete until the pieces gather into one externally verified result.
