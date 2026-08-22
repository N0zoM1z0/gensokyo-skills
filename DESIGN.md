# Design contract

## Thesis

Gensokyo Skills translates character motifs into problem-solving workflows that are simultaneously:

- **distinct** — the selected character changes the reasoning path;
- **testable** — quality and routing can fail in observable ways;
- **composable** — one skill can hand a bounded artifact to another;
- **self-contained** — installing one skill never requires the repository root;
- **provenanced** — canon inspiration, fan interpretation, and original procedure stay distinguishable.

The project optimizes for useful behavior first and memorable framing second. Both are required.

## Five-layer model

| Layer | Meaning | Example |
| --- | --- | --- |
| Character | Cognitive policy with strengths and bias | Reimu converges toward a normal state. |
| Spell card | Operator that changes an artifact or decision | Classify observations into signal, consequence, noise, and unknown. |
| Skill | Executable workflow with routing and exit criteria | `reimu-incident-triage` |
| Incident | Task or eval that exposes behavioral differences | Intermittent CI failure after parallelization. |
| Party | Composition with an explicit handoff | Marisa produces evidence; Reimu consumes it for recovery. |

Character and skill deliberately remain many-to-many. A character may support more than one useful workflow later, and a capability is not canon merely because the project maps it to a character.

## Admission tests

### Deletion test A: remove Touhou

Delete the character name, spell-card labels, and Gensokyo vocabulary. The remainder must still contain a precise workflow, decision delta, failure mode, and completion test. “Analyze carefully” fails.

### Deletion test B: swap the character

Replace the mapped character with another. If the procedure still fits unchanged, the character is only a skin. Reimu must converge and restore; Marisa must experiment and learn; Cirno must strip and stress; Yukari must trace crossings and contracts.

Aya must verify claims through source lineage; Nitori must reconstruct hidden mechanisms through controlled probes; Eiki must apply an authoritative rule with proportional remedy; Seija must invert one load-bearing premise and reconcile the result with evidence.

Kogasa must produce a genuine behavioral surprise and forge it into a regression guard; Suika must scatter a defined whole across independent seams and gather it through explicit contracts; Sakuya must advance risky state transitions through observable checkpoints while admitting irreversibility.

### Operator test

Every named operator must change at least one of:

- agent state;
- task artifact;
- evidence set;
- candidate decision;
- scope boundary.

A decorative heading fails.

### Bias test

Every skill must say what it overdoes. Add a countercheck that preserves the useful bias while catching its characteristic failure. A skill with only strengths will drift back toward generic assistant behavior.

## Runtime package contract

Each directory under `skills/` must stand alone and contain:

```text
SKILL.md
agents/openai.yaml
references/provenance.md
references/worked-example.md
evals/cases.json
```

Keep only `name` and `description` in `SKILL.md` frontmatter. Put discovery boundaries in `description`; clients cannot route on instructions they have not loaded. Put project-specific fingerprints in `catalog/`, not nonportable frontmatter.

Keep lore outside the core procedure. Link provenance only for users who ask about the mapping or fanwork basis. The runtime workflow must not depend on character biography.

## Utility workflow contract

The repository may ship a small non-character utility when it supports the character workflows without inventing a ninth cognitive policy. Utilities still use the complete runtime package shape and must have routing, near-miss, and quality evals, but they:

- live in `catalog/skills.json` under `utilities`, outside character fingerprints;
- do not join parties or character contrast incidents;
- do not borrow a character name merely for theme;
- must state a narrow operational trigger and a guardrail against ambient activation.

`gensokyo-commit-attribution` is the reference case: it records material character-workflow provenance at commit time but contributes no problem-solving policy of its own.

## Routing contract

For every runtime package, write:

- realistic prompts that should trigger it;
- near-miss prompts that should select another named skill;
- prompts where no Gensokyo skill is appropriate;
- quality cases that inspect decision structure, not phrasing.

Descriptions must state both positive and negative boundaries. Avoid routing on character names alone.

## Contrast contract

Run the same incident through multiple character skills. Expected differences must concern action:

- what evidence is sought;
- how scope is changed;
- which artifact is produced;
- what decision becomes possible;
- when the workflow stops.

Different vocabulary with the same plan is a failed contrast.

## Model eval contract

Static validation protects package shape. Model evals protect behavior at three different boundaries:

| Mode | Question | Pass signal |
| --- | --- | --- |
| Routing | Does the description select the right skill—or none—without loading its body? | Exact annotated skill id. |
| Quality | Does loading the skill materially improve the answer? | Blinded skill answer covers every requirement, violates no prohibition, clears the score floor, and beats baseline. |
| Contrast | Does each skill make a different useful move on the same incident? | Every annotated move appears and all compared decision shapes remain distinct. |

Quality comparisons randomize the A/B label deterministically so the judge never receives a `baseline` or `with_skill` label. Rubrics describe observable behavior rather than exact phrasing. Contrast annotations are commitments: changing a skill may require changing the expected move, but never merely to turn a failing run green.

Model judgments are evidence, not an oracle. Keep the candidate and judge models in the run artifact, inspect failures, rerun suspicious cases, and use human review before changing a routing boundary or admission decision. See [EVALS.md](EVALS.md).

## Composition contract

Use one skill by default. Use two for complementary policies and three only when the third contributes a decision the first two cannot.

Every composition must define:

- order or coordination rule;
- what the sender provides;
- what the receiver expects;
- what artifact ends the handoff.

Four or more skills are rejected unless the project changes this design contract explicitly. This prevents a themed council from consuming more attention than the task.

## Fanwork contract

Keep the mapping in three explicit steps:

1. **source anchor** — the upstream or official characterization that inspired the mapping;
2. **interpretive bridge** — the cognitive motif inferred by this fan project;
3. **project-original operator** — the actual procedure shipped here.

Never state that a modern professional capability is canon. Do not ship extracted game assets, music, sprites, copied dialogue, or unlicensed fan material. See [FANWORK_NOTICE.md](FANWORK_NOTICE.md).
