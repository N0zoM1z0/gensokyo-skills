---
name: cirno-radical-simplification
description: Strip an overcomplicated plan to a working design with at most three moving parts, expose the first real constraint that breaks it, and add complexity back only when justified. Use for architecture sprawl, tool overload, premature scaling, tangled workflows, or plans nobody can explain simply. Do not use to dismiss necessary safety, compliance, evidence, or domain complexity.
---

# Cirno Radical Simplification

Treat the character framing as a mnemonic for a working method. Do not role-play unless the user asks.

## Objective

Find the strongest simple plan that survives contact with the real constraints.

Simple means fewer independent failure points and decisions, not fewer words or less care.

## Operating bias

- Freeze scope before discussing machinery.
- Demand a baseline with no more than three moving parts.
- Remove speculative flexibility, scale, and indirection.
- Reintroduce complexity one constraint at a time.

## Required context

Identify:

- the single outcome that must work;
- explicit non-goals;
- current moving parts and dependencies;
- hard constraints versus forecasts and preferences;
- the cost of failure and any non-negotiable safeguards.

Count a moving part when it can fail, be deployed, be owned, or change independently.

## Procedure

### Cold Sign — Scope Lock

Rewrite the request as one observable outcome. Freeze new features for the duration of the analysis. Move every desirable but nonessential outcome into `not now`.

Do not freeze safety, legal, data-integrity, or user-consent constraints.

### Frost Sign — Three-Part Solution

Propose a baseline containing at most three moving parts. Prefer, in order:

1. an existing capability;
2. one process with direct storage;
3. a small composition of well-understood parts.

For every removed component, state what job it supposedly performed and how the baseline handles or deliberately rejects that job.

### Ice Test — Find the first crack

Stress the baseline against actual constraints. Test concrete cases such as:

- required throughput or latency;
- isolation and permissions;
- durability and recovery;
- coordination across owners;
- offline or partial failure;
- compliance and auditability.

Stop at the first constraint the simple plan genuinely cannot satisfy. Distinguish measured constraints from imagined future needs.

### Thawing Rule — Earn each addition

Add one component or abstraction only when it resolves a named failed constraint. Record:

- the constraint;
- why the baseline fails it;
- the smallest added mechanism;
- the new failure mode and operating cost;
- how success will be measured.

Repeat only while a hard constraint remains unsatisfied.

## Characteristic failure mode

This method can oversimplify and recast missing capability as elegance.

Before finishing, run the necessity countercheck:

- Did the plan silently drop a required user or failure case?
- Is complexity intrinsic to the domain rather than accidental in the design?
- Would the simple plan concentrate unacceptable operational or human risk?
- Can a domain expert name a constraint the baseline has not faced?

If the disagreement is about an interface or ownership line, hand off to boundary analysis rather than adding arbitrary machinery.

## Output contract

Return:

1. **Frozen outcome** — required result, hard constraints, non-goals.
2. **Moving-part inventory** — current parts and independent failure points.
3. **Three-part baseline** — simplest credible plan.
4. **What disappeared** — removed parts and their former jobs.
5. **First real constraint** — the first evidence-backed failure of the baseline.
6. **Earned complexity** — additions tied one-to-one to constraints.
7. **Strongest simple plan** — final design and remaining risks.

## References

Read [references/provenance.md](references/provenance.md) only when explaining the character-to-workflow mapping or reviewing fanwork provenance. Read [references/worked-example.md](references/worked-example.md) when “simple” is being confused with “under-specified.”
