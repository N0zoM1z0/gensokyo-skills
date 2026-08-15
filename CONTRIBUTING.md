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
- one quality case with a stable slug `id`, observable requirements, and explicit failure criteria;
- a catalog entry and at least one cross-skill contrast expectation.

Do not add a composition solely because two characters have a relationship. Define a useful handoff contract and keep the party at three skills or fewer.

## Acceptance checklist

- The workflow passes both deletion tests.
- Every spell/operator changes state, evidence, scope, an artifact, or a decision.
- The output contract differs materially from neighboring skills.
- The failure mode and countercheck are specific to the skill's bias.
- The package contains no extracted official assets or copied dialogue.
- `python3 scripts/validate.py` passes.
- `python3 -m unittest discover -s tests -v` passes.
- `python3 scripts/eval_model.py dry-run --kind quality --skill <skill-id>` resolves the intended case and request count.
- `npx skills add . --list` discovers the intended public skills.

Run a real task with and without the skill before requesting review. For a complex skill, also compare its output against the nearest neighboring character using the same incident. When API credentials are available, use the model runner described in [EVALS.md](EVALS.md) and attach the result artifact or summarize its exact model ids, case selection, and failures.

## Distribution contract

Keep public skill folders under `skills/<skill-id>/`; this is the canonical layout discovered by the Agent Skills CLI and the OpenAI plugin. When a release changes installed behavior, bump the semantic version in `.codex-plugin/plugin.json`. Keep `.agents/plugins/marketplace.json` pointed at the public `main` branch and let CI verify the CLI discovery path.

Do not add an npm wrapper package solely to ship these files. `npx skills` is the installer; the skill source remains this repository. An npm plugin package is a separate optional distribution channel and should be added only with a real release and ownership plan.
