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

## Routing contract

For every skill, write:

- realistic prompts that should trigger it;
- near-miss prompts that should select another named skill;
- prompts where no Gensokyo skill is appropriate;
- quality cases that inspect decision structure, not phrasing.

Descriptions must state both positive and negative boundaries. Avoid routing on character names alone.

## Contrast contract

Run the same incident through multiple skills. Expected differences must concern action:

- what evidence is sought;
- how scope is changed;
- which artifact is produced;
- what decision becomes possible;
- when the workflow stops.

Different vocabulary with the same plan is a failed contrast.

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
