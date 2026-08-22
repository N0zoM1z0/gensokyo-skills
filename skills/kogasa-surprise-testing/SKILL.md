---
name: kogasa-surprise-testing
description: Discover plausible inputs, state transitions, orderings, and dependency behaviors that violate an expected contract, prove the smallest genuine surprise, and forge it into a deterministic regression test. Use for edge-case design, negative testing, failure injection, fragile happy paths, or bugs that need a durable test. Do not use for purely conceptual assumption challenges, open-ended feasibility spikes, incident recovery, or exhaustive test-plan generation without a defined oracle.
---

# Kogasa Surprise Testing

Treat the character framing as a mnemonic for a working method. Do not role-play unless the user asks.

## Objective

Turn one decision-relevant surprise into a reproducible counterexample and a durable regression guard.

## Operating bias

- Attack expectations at behaviorally meaningful seams, not with random oddities.
- Prefer one observed counterexample over a long speculative edge-case list.
- Change one condition at a time and preserve the exact input, state, and environment.
- Finish by forging the surprise into an executable oracle whenever the artifact permits it.
- Own the regression artifact and its evidence; do not turn testing into the surrounding release, adoption, or architecture decision.

## Required context

Collect what is already available before asking questions:

- the behavior, contract, invariant, or user promise under test;
- a normal example and its expected observation;
- available test surfaces, fixtures, logs, and failure-injection controls;
- state and lifecycle assumptions, including retries and cleanup;
- prior failures and high-cost consequences;
- safety, authorization, time, and execution constraints.

If no oracle distinguishes acceptable from broken behavior, define or obtain one before generating cases. Do not call merely unusual behavior a defect.

Derive the oracle independently of the implementation path under test: use the written contract, a small reference transformation, an invariant over durable state, or another separately observable effect. “The function returned the expected result” is an observation, not an independent oracle, when that same function defines the result being questioned.

## Procedure

### Closed Umbrella — Fix the expectation

Write a compact contract ledger. For each relevant promise, record:

- precondition;
- action or transition;
- invariant or expected result;
- observable oracle;
- consequence if violated.

Choose one promise whose failure would change a decision. Keep the normal case as a control.

### Surprise Sign — Turn one expectation sideways

Generate a small ranked set of plausible surprises across the surfaces that actually exist:

- boundary value or malformed input;
- representation, encoding, or normalization;
- ordering, concurrency, retry, or duplication;
- lifecycle state, interruption, or partial completion;
- dependency delay, error, stale response, or inconsistent response;
- recovery and cleanup behavior.

For every candidate, state the expectation it challenges, why the condition is plausible, the smallest safe probe, and the decisive observation. Rank by consequence, plausibility, and discrimination. Do not enumerate every combination.

If the user asks for an arbitrary case count or calls an exhaustive novelty list “complete,” explicitly decline that completeness claim. State the evidence-based stopping rule, then return only the few ranked cases that can change a decision.

### Genuine Scream — Prove the smallest surprise

Run the safest discriminating probe when authorized and practical. Otherwise specify it exactly without claiming execution.

Change one condition from the control. Capture:

- exact input and initial state;
- environment and dependency behavior;
- expected versus observed result;
- repeat count and consistency;
- evidence that the result is a contract violation rather than a valid surprise.

Minimize the counterexample while preserving the failure. If it disappears, record the lost condition instead of inventing certainty.

### Tatara Forge — Make the surprise durable

Encode the counterexample at the lowest stable layer that can express the contract. Produce:

1. deterministic setup;
2. one triggering action;
3. a precise assertion or oracle;
4. isolated cleanup;
5. a name that describes the violated promise.

Remove irrelevant timing, global state, and oversized fixtures. Keep the original observation beside the test when the test substitutes a lower-level oracle.

The maintained regression guard—not a disposable timeboxed spike—is this workflow's completion artifact. If the only available outcome is an experiment that decides whether a new approach is feasible, hand that question to rapid prototyping instead of relabeling the spike as a regression.

### Encore Check — Test the test

Demonstrate that the guard is meaningful:

- reproduce the failure on the unfixed behavior or with controlled fault injection;
- observe the test pass on the corrected behavior;
- repeat enough times to expose timing flakiness;
- perturb an irrelevant condition and confirm the result does not change;
- record adjacent surfaces that remain untested.

Stop when one consequential surprise is reproducible, minimized, encoded, and shown to discriminate broken from acceptable behavior.

The forged guard is the completion artifact. Report what it proves and what remains untested, then return the wider proceed, modify, stop, release, or redesign decision to its owner. Do not prescribe a production fix merely because the regression exposes where a fix may belong.

## Characteristic failure mode

This method can chase novelty, produce theatrical edge cases with no realistic path, or mistake surprising-but-valid behavior for a bug.

Before keeping a case, perform one relevance countercheck:

- Which contract, historical failure, or credible operating condition makes this case matter?
- Is the oracle independent of the implementation detail being tested?
- Would this test still protect behavior after an internal refactor?
- Did the search stop after decisive coverage, or continue only because more surprises were possible?
- Did the workflow remain a testing craft, or silently take over the product, release, or architecture decision?

Use assumption inversion when the disputed object is a premise rather than running behavior. Use rapid prototyping when the question is whether an approach is feasible at all. Use incident triage when restoration is the immediate goal.

## Output contract

Return:

1. **Expectation ledger** — selected contract, control, independently derived oracle, consequence. Name how the oracle is computed or observed outside the implementation path under test; do not relabel the subject's own return value as independent.
2. **Ranked surprises** — plausible variations with rationale and safe probes.
3. **Minimal counterexample** — exact state, changed condition, observation, reproducibility.
4. **Forged regression** — setup, action, assertion, cleanup, and target layer.
5. **Forge proof** — fail-before or fault-injected evidence, pass-after evidence, stability check.
6. **Residual blind spots** — important surfaces not covered and why.

When execution is unavailable, label the counterexample and regression as proposed rather than observed.
State the evidence threshold the regression supplies, but do not replace the caller's broader decision policy with a testing opinion.

## References

Read [references/provenance.md](references/provenance.md) only when explaining the character-to-workflow mapping or reviewing fanwork provenance. Read [references/worked-example.md](references/worked-example.md) when surprise generation is drifting into an unranked edge-case list.
