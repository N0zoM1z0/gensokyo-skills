---
name: nitori-reverse-engineering
description: Reconstruct how an existing artifact or system works by inventorying observable surfaces, mapping interfaces and flows, forming competing mechanism hypotheses, probing them safely, and building a minimal explanatory replica. Use for undocumented formats, protocols, binaries, devices, legacy behavior, compatibility work, or mysterious black boxes. Do not use for choosing whether a new idea is feasible or for bypassing authorization and access controls.
---

# Nitori Reverse Engineering

Treat the character framing as a mnemonic for a working method. Do not role-play unless the user asks.

## Objective

Produce the smallest testable mechanism model that explains the observed behavior and predicts a new result.

## Operating bias

- Inspect the artifact before trusting stories about it.
- Make interfaces, state, energy/data flow, and failure behavior visible.
- Change one input at a time and preserve reproducible observations.
- Prefer a working explanatory replica over confident mechanism prose.

## Authorization and safety boundary

Confirm that inspection, interoperability testing, traffic capture, disassembly, or modification is authorized. Avoid credential bypass, destructive probing, unsafe hardware states, privacy violations, and redistribution of proprietary material. Use isolated copies and sanitized captures when possible.

## Required context

Collect:

- the artifact, version, hash, build, or physical configuration;
- known inputs, outputs, controls, and environment;
- one observed behavior the model must explain;
- available source, documentation, logs, traces, samples, or tools;
- legal, safety, clean-room, and compatibility constraints;
- the desired fidelity: understand, interoperate, reproduce, repair, or modify.

## Procedure

### Tool Bench — Inventory the artifact

Preserve an untouched reference. Record identifiers, file structure, exposed symbols, endpoints, connectors, dependencies, and baseline behavior. Separate observation from interpretation.

### Pipe Map — Follow matter, data, and state

Draw a mechanism map:

- inputs and their representations;
- transformations and persistent state;
- outputs and externally visible side effects;
- control, timing, error, and reset paths;
- trust, process, network, or physical boundaries.

Mark each edge as observed, documented, inferred, or unknown.

### Gear Hypothesis — Offer competing mechanisms

For every important unknown, write at least two plausible explanations when evidence permits. For each hypothesis, predict an observation that differs from the alternatives.

Do not let familiar architecture names substitute for evidence.

### Pressure Test — Probe one variable

Choose the safest discriminating probe. Vary one dimension such as input length, order, timing, version, state, encoding, load, or failure condition. Capture exact setup and result.

Use static inspection before dynamic execution when unknown code or hardware may be unsafe. Add instrumentation at the narrowest useful boundary.

### Workshop Replica — Make the model run

Build a minimal parser, emulator, state machine, mock, circuit sketch, or compatibility shim that reproduces the key observation. Then test one novel case not used to construct it.

Classify the model as:

- `descriptive`: fits observations;
- `predictive`: correctly predicts a new result;
- `operational`: supports the required interoperability or repair;
- `inconclusive`: alternatives remain indistinguishable.

### Warning Label — Expose the unknowns

List unsupported paths, version sensitivity, safety limits, copied assumptions, and cleanup needs. Distinguish a useful model from a complete reconstruction.

## Characteristic failure mode

This method can become attached to an elegant mechanism, understate prototype risk, or inspect deeper than the user is authorized to go.

Before finishing, perform one workshop safety check:

- What observation would prove the model wrong?
- Was the novel prediction truly independent of the fitting data?
- Did any probe change or damage the artifact?
- Can the result be shared without exposing secrets or proprietary material?

If the question is only whether a proposed approach can work, hand off to rapid prototyping. If the failure is already localized and recovery is urgent, hand off to incident triage.

## Output contract

Return:

1. **Artifact inventory** — identity, environment, preserved baseline.
2. **Observable interface map** — inputs, state, outputs, and boundaries.
3. **Mechanism hypotheses** — evidence and differentiating predictions.
4. **Probe log** — one-variable tests and observations.
5. **Minimal replica** — what it explains and the novel prediction.
6. **Confidence and warning label** — unknowns, limits, safety, and next probe.

## References

Read [references/provenance.md](references/provenance.md) only when explaining the character-to-workflow mapping or reviewing fanwork provenance. Read [references/worked-example.md](references/worked-example.md) when an inferred mechanism has not yet made a novel prediction.
