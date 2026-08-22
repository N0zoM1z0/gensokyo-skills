---
name: sakuya-checkpointed-execution
description: Convert a risky multi-step operation into a dependency-ordered runbook with observable checkpoints, irreversible-action gates, honest rollback or compensation paths, abort conditions, and end-to-end verification. Use for deployments, migrations, cutovers, key rotations, bulk transformations, or maintenance where partial failure matters. Do not use for diagnosing an unknown incident, generic calendar planning, parallel work decomposition, or low-risk implementation with no meaningful state transition.
---

# Sakuya Checkpointed Execution

Treat the character framing as a mnemonic for a working method. Do not role-play unless the user asks.

## Objective

Advance a risky operation through bounded, observable state transitions without pretending that every action can be undone.

## Operating bias

- Order work by state dependency, not by a convenient checklist.
- Observe and record each checkpoint before time advances to the next transition.
- Separate rollback, roll-forward, and compensation; none is automatic recovery.
- Put explicit human or policy gates before irreversible impact.

## Required context

Collect what is already available before asking questions:

- current state, target state, and invariants that must remain true;
- systems, data, users, and regions in scope;
- dependencies and compatibility windows;
- authority, approvers, operators, observers, and communication channels;
- backup, restore, replay, compensation, and failover capabilities;
- maintenance window, time bounds, and external deadlines;
- monitoring signals and original user paths used for verification.

Do not convert unknowns into implied permission. If a prerequisite changes whether an action is safe, make it a blocking precondition.

Before producing a checkpointed runbook, verify that the request contains a meaningful risky state transition: partial failure, live compatibility, costly recovery, external side effects, or irreversible impact. If ordinary version control and normal review make every effect cheap to reverse, stop this workflow and return only a proportionate edit-review-check path. Do not reproduce minute-by-minute scheduling, executive gates, recovery matrices, or extended observation merely because the user requested operational ceremony.

## Procedure

### Clock Face — Freeze the state model

Record:

- current state and evidence timestamp;
- target state;
- invariants and allowed temporary degradations;
- entry criteria and excluded scope;
- completion deadline or compatibility window;
- global abort conditions.

Identify assumptions that can expire during the run. Assign a refresh point to volatile observations such as replication lag, capacity, active traffic, and backup freshness.

### Silver Sequence — Order the transitions

Build a dependency graph, then express each step with:

1. preconditions;
2. authorized action;
3. expected state transition;
4. immediate success signal;
5. maximum observation window;
6. owner;
7. next step on success;
8. stop, rollback, or compensate path on failure.

Do not continue past a step whose resulting state is unknown. Separate preparation, reversible activation, cutover, and cleanup.

### Time Stop — Establish real checkpoints

Before every consequential transition, capture a recovery point that can actually be used. Classify the step as:

- `reversible`: the prior state can be restored within the required window;
- `compensatable`: the prior state cannot be restored, but a defined action can repair its material effects;
- `irreversible`: neither restoration nor adequate compensation is available.

For any claimed rollback, state what data or state it restores, what it does not restore, the time required, and how restoration was tested. A down migration, backup file, Git revert, or retained binary is not proof of recoverability by itself.

### Red Knife Gate — Admit irreversibility

Before a compensatable or irreversible step, require:

- named authority to proceed;
- fresh checkpoint evidence;
- impact and blast-radius statement;
- communication or maintenance condition;
- explicit go/no-go criteria;
- the last safe abort point;
- selected roll-forward or compensation plan.

Stop for authorization when the user has not granted it. Never hide a destructive transition inside an otherwise routine step.

### Perfect Interval — Advance one window

Execute only the authorized window. Record planned versus actual:

- start and finish time;
- operator and artifact version;
- precondition evidence;
- action result;
- checkpoint signal;
- deviation and decision.

On failure, freeze progress at the current known state. Apply the preselected rollback or compensation only when its own preconditions still hold. If neither path is safe, contain impact and escalate rather than improvising forward.

### Maid's Check — Verify the lived result

Verify:

- the original external user or system path;
- target-state invariants;
- unchanged critical paths;
- data consistency and background work;
- monitoring after at least one relevant operating interval;
- cleanup of compatibility scaffolding only after its exit condition.

Record residual risk, follow-up owner, and the trigger for removing temporary safeguards. Stop when the target state is verified and no transition remains half-open.

## Characteristic failure mode

This method can confuse precise scheduling with control, produce a ceremonial runbook, or assume that a checkpoint makes an irreversible event reversible.

Before approving the sequence, perform one time-reality countercheck:

- Was each rollback restored in a representative environment, or merely documented?
- Can state change between the checkpoint observation and the action?
- Are time estimates based on current scale and throughput?
- Does the plan define what happens when a step exceeds its observation window?
- Is cleanup delayed until compatibility consumers have actually left?

Use incident triage when an unexplained failure is already active. Use scatter-gather planning when independent workers need bounded ownership. Use boundary analysis when the unresolved problem is an interface contract.

## Output contract

For a meaningful risky state transition, return:

1. **State model** — current, target, invariants, allowed degradation, scope, abort conditions.
2. **Checkpointed runbook** — ordered steps with preconditions, action, signal, window, owner, and failure path.
3. **Recovery matrix** — reversible, compensatable, or irreversible; recovery scope, evidence, duration, limits.
4. **Go/no-go gates** — authority, fresh evidence, impact, last safe abort point.
5. **Execution record** — planned versus actual state when actions are performed.
6. **Final verification** — external path, invariants, operating interval, residual risk, cleanup trigger.

For a low-risk change with no meaningful transition, do not emit this full structure. Briefly explain the classification, give the normal lightweight workflow, and stop.

When the user requests a plan only, do not execute the operation. When execution is authorized, pause at every stated gate.

## References

Read [references/provenance.md](references/provenance.md) only when explaining the character-to-workflow mapping or reviewing fanwork provenance. Read [references/worked-example.md](references/worked-example.md) when a rollback claim depends on an untested backup, down migration, or configuration revert.
