---
name: reimu-incident-triage
description: Isolate the real abnormal condition in a noisy incident, reduce it to the smallest relevant scope, and choose a minimal reversible recovery with explicit verification. Use for regressions, outages, flaky failures, broken workflows, or messy bug reports with many symptoms and competing explanations. Do not use for open-ended invention, routine implementation, or interface design when no incident exists.
---

# Reimu Incident Triage

Treat the character framing as a mnemonic for a working method. Do not role-play unless the user asks.

## Objective

Restore a known-good condition without being recruited into every nearby problem.

## Operating bias

- Converge from symptoms toward one observable abnormality.
- Prefer direct evidence, a narrow scope, and reversible intervention.
- Preserve unrelated behavior that is already working.
- Stop after restoration is verified and residual risk has an owner.

## Required context

Collect what is already available before asking questions:

- expected behavior and observed behavior;
- impact and urgency;
- last known-good and first known-bad state;
- recent changes;
- reproduction evidence, logs, screenshots, or failing checks;
- actions already tried and their results.

Ask only for missing information that changes the next safe action. When evidence is unavailable, state the uncertainty and propose the cheapest discriminating observation.

## Procedure

### Purification Sign — Sort the scene

Create an observation ledger. Classify each item as:

- `abnormality evidence`: directly distinguishes working from broken;
- `consequence`: damage caused by the abnormality, but not the cause;
- `context`: relevant constraint or environment fact;
- `unrelated noise`: tempting but unsupported side issue;
- `unknown`: potentially relevant, not yet tested.

Do not discard a safety, security, or data-integrity signal as noise merely because it is inconvenient.

### Boundary Sign — Draw the incident

Write one sentence in this form:

> After `<change or transition>`, `<smallest affected scope>` does `<observed behavior>` instead of `<expected behavior>` under `<conditions>`.

Then identify:

1. the first known-bad point;
2. changed and unchanged components;
3. the smallest reproducible boundary that still contains the failure;
4. one observation that would shrink the boundary further.

If there is no reproducible boundary, improve observability before proposing a broad rewrite.

### Resolution Sign — Restore normality

Rank plausible causes by evidence, not narrative appeal. For the leading cause, choose the smallest action that:

1. can plausibly remove or bypass the abnormal condition;
2. is reversible or has a rollback;
3. preserves unrelated working behavior;
4. produces an observable success or failure signal.

Separate `containment`, `recovery`, and `permanent correction`. Do not call a workaround a root-cause fix.

### Shrine Check — Verify and leave cleanly

Verify the original failure path, not only a proxy. Record:

- evidence that normal behavior returned;
- anything not explained;
- recurrence or systemic risk;
- follow-up owner and trigger, when follow-up is justified.

Stop investigating when the abnormal condition is bounded, recovery is verified, and remaining risk is explicit.

## Characteristic failure mode

This method can converge too early and mistake local recovery for systemic safety.

Before finishing, perform one countercheck:

- Could the same cause affect other users, data, regions, or components?
- Did the recovery hide the signal rather than remove the condition?
- Does recurrence indicate a structural boundary problem?

Hand off repeated cross-component failures to a boundary analysis. Hand off uncertain solution ideas to a rapid prototype.

## Output contract

Return these sections, omitting none unless the user requests another format:

1. **Actual incident** — expected versus observed, affected scope, impact.
2. **Signal ledger** — evidence, consequences, noise, unknowns.
3. **Leading explanation** — claim, supporting evidence, disconfirming test.
4. **Smallest safe action** — containment or correction, rollback, owner.
5. **Verification** — exact success signal and residual risks.

Keep unrelated improvements in a short parking-lot section. Do not silently implement them.

## References

Read [references/provenance.md](references/provenance.md) only when explaining the character-to-workflow mapping or reviewing fanwork provenance. Read [references/worked-example.md](references/worked-example.md) when the distinction between symptom cleanup and incident restoration is unclear.
