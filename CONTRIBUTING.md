# Contributing

Start with a behavior gap, not a favorite character.

## Propose a skill

Open an issue or draft a package that answers:

1. What user request should trigger this skill?
2. What decision or artifact does it produce that the current cast does not?
3. Which character motif makes this workflow more memorable and precise?
4. What does this cognitive policy overdo?
5. Which existing skill should win the closest routing near-miss?

## Required package

Copy the structure described in [DESIGN.md](DESIGN.md). Keep `SKILL.md` concise, imperative, and self-contained. Its frontmatter must contain only `name` and `description`.

Add:

- a provenance note separating source anchor, interpretation, and original operators;
- one worked example that demonstrates the decision delta;
- at least three should-trigger cases;
- at least three near-miss or should-not-trigger cases;
- one quality case with observable requirements;
- a catalog entry and at least one cross-skill contrast expectation.

Do not add a composition solely because two characters have a relationship. Define a useful handoff contract and keep the party at three skills or fewer.

## Acceptance checklist

- The workflow passes both deletion tests.
- Every spell/operator changes state, evidence, scope, an artifact, or a decision.
- The output contract differs materially from neighboring skills.
- The failure mode and countercheck are specific to the skill's bias.
- The package contains no extracted official assets or copied dialogue.
- `python3 scripts/validate.py` passes.

Run a real task with and without the skill before requesting review. For a complex skill, also compare its output against the nearest neighboring character using the same incident.
