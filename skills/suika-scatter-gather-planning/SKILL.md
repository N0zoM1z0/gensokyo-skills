---
name: suika-scatter-gather-planning
description: Decompose one bounded deliverable into genuinely independent work packets, give each packet an ownership and evidence contract, and recombine the results through an explicit merge order and integrated acceptance check. Use for parallel contributors, subagents, multi-package changes, or large work with real dependency seams. Do not use to delete unnecessary complexity, diagnose a failing interface, schedule one sequential operator, or manufacture parallelism for a small task.
---

# Suika Scatter-Gather Planning

Treat the character framing as a mnemonic for a working method. Do not role-play unless the user asks.

## Objective

Scatter work only where independence is real, then gather every required result into one verified whole.

## Operating bias

- Define the whole and its invariants before dividing it.
- Split along dependency and ownership seams, not equal-looking task counts.
- Give each worker a bounded artifact and a proof obligation.
- Design the gathering contract before parallel work begins.

## Required context

Collect what is already available before asking questions:

- final deliverable and integrated acceptance test;
- required behavior, interfaces, constraints, and non-goals;
- repository or artifact ownership boundaries;
- available workers, tools, permissions, and time limits;
- known dependencies, shared resources, and likely conflicts;
- decisions that must remain centralized.

Do not split a task whose acceptance condition is still ambiguous. Clarify the whole first.

Before producing scatter/gather artifacts, check whether the task has at least two honest seams whose parallel-time saving exceeds the coordination cost. If it does not, stop this workflow and return only the ordinary single-owner path. Do not add a coordinator, status packets, standby workers, or a merge ceremony after rejecting the split; those are still manufactured parallelism.

## Procedure

### Gathering Sign — Name the whole

Write one completion statement for the final deliverable. Record:

- invariants every packet must preserve;
- the integrated acceptance test;
- shared terminology, schemas, versions, and assumptions;
- decisions that only one owner may make;
- work that is explicitly out of scope.

This whole-state contract is the reference used when scattered results disagree.

### Sparse Fog — Find honest seams

Build a small dependency graph. Mark:

- independent leaves that can begin immediately;
- interface-defining work that must finish first;
- shared files, state, environments, or decision rights;
- the indivisible core whose parts would require constant coordination;
- downstream work blocked on an explicit artifact.

Prefer vertical packets that can be verified on their own. Keep tightly coupled work together even when that produces unequal packet sizes.

A downstream packet may still be honest when it cannot start immediately, but it must save real critical-path work and return an independently reviewable artifact. Available workers alone never justify a packet.

### Oni Scatter — Issue bounded work packets

For each packet, specify:

1. **Goal** — one observable contribution to the whole.
2. **Inputs** — frozen context and upstream artifacts.
3. **Owned scope** — files, modules, records, or decisions it may change.
4. **Forbidden overlap** — shared surfaces it must not modify independently.
5. **Output** — exact artifact or decision to return.
6. **Evidence** — local checks that establish packet completion.
7. **Dependencies** — blockers and consumers.
8. **Return condition** — done, blocked, or invalidated, with no hidden partial state.

Use no more packets than there are independent seams and capable workers. A packet consisting only of “investigate” must name the evidence it will return.

### Oni's Promise — Fix the gathering contract

Before work proceeds, establish:

- canonical interface and schema owners;
- naming, formatting, and version rules;
- conflict resolution authority;
- merge readiness checks;
- how rejected or stale packets are handled;
- one place where integration decisions are recorded.

Do not let several workers make incompatible edits to a shared contract and defer the choice to merge time.

### Feast Sign — Gather in dependency order

Integrate in this order unless the dependency graph proves another:

1. shared contracts and interfaces;
2. independent producer artifacts;
3. consumers and adapters;
4. documentation and operational surfaces;
5. the integrated acceptance test.

Validate each packet at its boundary before merging it. After gathering, test the whole from an external user or system path; a set of locally passing packets is not yet a completed deliverable.

Name that external path concretely. Schema validators, unit checks, generated fixtures, and snapshots are integration evidence, but they do not replace a rendered, runtime, published, or consuming-system check when such a path defines success.

Stop when every required packet is accepted or explicitly discarded, conflicts are resolved by the named owner, and the integrated acceptance test passes.

## Characteristic failure mode

This method can over-split work, create coordination theater, or hide one coupled task behind many status reports.

Before scattering, perform a merge-tax countercheck:

- Can the packet progress without continuous answers from another packet?
- Is its output independently reviewable and testable?
- Does the expected parallel-time saving exceed briefing, synchronization, and merge cost?
- Would keeping two packets together reduce shared-file or shared-decision collisions?
- Is one coordinator becoming the bottleneck for every small decision?

Merge packets back together when independence is not earned. Use radical simplification when the work itself is unnecessary. Use boundary analysis when the problem is a failing crossing rather than work allocation. Use checkpointed execution when one operator must perform a risky sequence.

## Output contract

When at least one split is retained, return:

1. **Whole-state contract** — final deliverable, invariants, non-goals, integrated acceptance.
2. **Dependency map** — leaves, interfaces, shared state, indivisible core.
3. **Work packets** — goal, inputs, owned scope, forbidden overlap, output, evidence, dependencies, return condition.
4. **Gathering contract** — interface owners, conflict authority, readiness checks.
5. **Merge sequence** — dependency-ordered integration and per-boundary checks.
6. **Merge-tax judgment** — splits kept, recombined, or rejected with reasons.

When every proposed split is rejected, do not emit the full scatter/gather structure. State why the task is indivisible, name one owner, give the shortest completion-and-verification path, and stop.

If execution begins, maintain packet status without expanding ownership silently.

## References

Read [references/provenance.md](references/provenance.md) only when explaining the character-to-workflow mapping or reviewing fanwork provenance. Read [references/worked-example.md](references/worked-example.md) when parallel work packets look independent on paper but collide during integration.
