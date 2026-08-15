---
name: marisa-rapid-prototyping
description: Convert an uncertain idea into the smallest runnable experiment, reuse relevant prior art, observe a decisive signal, and scale only after evidence. Use for spikes, proof-of-concepts, feasibility questions, unfamiliar libraries, or competing implementation approaches. Do not use when the main need is incident containment, exhaustive research, or production rollout planning.
---

# Marisa Rapid Prototyping

Treat the character framing as a mnemonic for a working method. Do not role-play unless the user asks.

## Objective

Buy the most decision-relevant evidence with the least prototype work.

## Operating bias

- Move from speculation to a runnable artifact quickly.
- Borrow proven parts before inventing new machinery.
- Prefer one sharp experiment over a broad imitation of the final product.
- Treat failed experiments as useful only when they change the next decision.

## Required context

Determine:

- the decision the prototype must unlock;
- the riskiest assumption behind that decision;
- the cheapest observable success and failure signals;
- constraints that must be real in the experiment;
- constraints that may be simulated;
- the sandbox, timebox, and cleanup boundary.

If the user asks to “prototype” but the choice is already settled, implement the requested slice instead of manufacturing uncertainty.

## Procedure

### Borrowed Magic — Search before shaping

Inspect the current codebase, official documentation, existing libraries, prior experiments, and nearby patterns. Produce a short reuse ledger:

- what can be reused unchanged;
- what can be adapted;
- what must be learned or built;
- license, security, or compatibility constraints that could invalidate reuse.

Do not copy an implementation without understanding the assumption being borrowed.

### Mini-Hakkero Test — Aim at one unknown

State one falsifiable hypothesis:

> If `<approach>` works under `<critical conditions>`, then `<observable signal>` will occur within `<time or resource bound>`.

Build the thinnest runnable path that can disprove it. Keep real only the interfaces necessary to test the risky assumption. Stub or omit presentation, scale, and polish unless one of them is the risk.

### Star Trail — Run and record

Run the experiment when safe and authorized. Capture:

- exact setup and command or interaction;
- observed result;
- deviations from the hypothesis;
- environmental assumptions;
- artifacts worth keeping.

Prefer an ugly measured result over a polished unmeasured demo.

### Master Spark Gate — Earn the larger build

Choose one outcome:

- `proceed`: evidence supports the approach;
- `modify`: evidence reveals a narrower viable approach;
- `stop`: the assumption failed or the expected value is too low;
- `inconclusive`: name the missing signal and the next smallest test.

Before turning a prototype into production work, require explicit decisions for tests, error handling, security, operability, migration, rollback, and cleanup.

## Characteristic failure mode

This method can create convincing demos that leave hidden prototype debt.

Before recommending adoption, perform one stabilization check:

- Which shortcuts would become incidents in production?
- Which dependency or copied pattern has not been verified?
- Which result depends on a toy dataset or friendly environment?
- What prototype artifact should be deleted rather than maintained?

Never test destructively in production or widen external side effects merely for speed.

## Output contract

Return:

1. **Decision at stake** — the choice this experiment informs.
2. **Risky assumption** — one falsifiable hypothesis.
3. **Borrowed parts** — reused evidence, code, tools, and constraints.
4. **Smallest experiment** — scope, steps, sandbox, timebox, signals.
5. **Observed result** — evidence, not impressions.
6. **Decision** — proceed, modify, stop, or inconclusive.
7. **Prototype debt** — shortcuts and the stabilization gate.

## References

Read [references/provenance.md](references/provenance.md) only when explaining the character-to-workflow mapping or reviewing fanwork provenance. Read [references/worked-example.md](references/worked-example.md) when a prototype is drifting into a miniature production build.
