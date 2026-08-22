# Model evaluations

`scripts/eval_model.py` turns the repository's JSON cases into executable model evaluations over the OpenAI Responses API. It uses only the Python standard library, sends `store: false`, and writes every result as JSON so a failure can be inspected rather than reduced to one score.

## What the four modes measure

### Routing

The router sees only each skill's `name` and `description`, matching how a client decides which instructions to load. Every should-trigger case must select its own skill. Every near-miss must select the annotated neighboring skill or `none`.

One case costs one candidate-model request.

### Quality

The candidate model answers the same task twice: once with generic baseline instructions and once with the selected `SKILL.md`. A separate judge receives those answers under a deterministic, blinded A/B order. The skill condition passes only when it:

- covers every `must_show` annotation;
- violates no `must_avoid` annotation;
- reaches the configured score floor; and
- beats the baseline rather than tying it.

One case costs two candidate requests and one judge request.

### Admission

The judge reviews a skill against the repository's deletion, swap, operator, artifact, and bias tests. The runner mechanically removes frontmatter, character terms, spell-card prefixes, and provenance links before presenting the deletion-test copy. The original procedure is compared against one deliberately chosen alternate character anchor, so names and lore cannot earn a pass by themselves.

An admission case passes only when:

- the stripped workflow remains precise and useful;
- the operator sequence fits the original character materially better than the swap character;
- operators change the annotated state, artifact, evidence, decision, or scope;
- the expected artifact is concrete rather than generic advice; and
- a characteristic overreach and operational countercheck are both present.

One case costs one judge-model request. Admission is a design audit, not a substitute for routing, task-quality, or same-incident contrast results.

### Contrast

The candidate answers one incident under every selected skill. The judge checks each annotated expected move and whether the resulting evidence requests, artifacts, decisions, scope changes, or stopping rules remain pairwise distinct. Vocabulary alone does not count.

One case costs one request per selected skill plus one judge request. Use repeated `--skill` filters to compare a focused pair before running the whole roster.
An incident may itself name only a focused nearest-neighbor set; validators require at least two known skills with distinct expected moves.

## Inspect without an API key

List every discovered case:

```bash
python3 scripts/eval_model.py list --kind all
```

Resolve selections and estimate request counts without making network calls:

```bash
python3 scripts/eval_model.py dry-run --kind routing
python3 scripts/eval_model.py dry-run --kind quality --skill aya-source-investigation
python3 scripts/eval_model.py dry-run --kind admission --skill kogasa-surprise-testing
python3 scripts/eval_model.py dry-run --kind contrast \
  --case parallel-ci \
  --skill reimu-incident-triage \
  --skill yukari-boundary-analysis
```

## Run against models

Set an API key, then begin with one case:

```bash
export OPENAI_API_KEY="..."
python3 scripts/eval_model.py run \
  --kind quality \
  --skill aya-source-investigation \
  --output eval-results/aya-quality.json
```

Run each suite independently:

```bash
python3 scripts/eval_model.py run --kind routing
python3 scripts/eval_model.py run --kind quality
python3 scripts/eval_model.py run --kind admission
python3 scripts/eval_model.py run --kind contrast
```

Useful controls:

- `--case <substring>` and `--skill <id>` are repeatable filters.
- `--limit N` bounds the selected case count.
- `--model` and `--judge-model` override repository defaults.
- `--reasoning-effort` and `--judge-reasoning-effort` override effort independently.
- `--api-base` targets an API-compatible test server; `OPENAI_BASE_URL` is also supported.
- `--no-fail` still records failures but returns a zero process status for exploratory runs.

Defaults live in [`evals/model-config.json`](evals/model-config.json). For a benchmark meant to be compared over time, pin dated model snapshots in a separate config or supply explicit overrides and retain the result artifact. A model alias can resolve differently later; the runner records both the requested and response model ids.

## Reading a result

The top-level summary reports case totals, pass rate, and accumulated input/output token usage. Each case preserves its prompts, model outputs, structured judgment, diagnostics, and pass flag. A live command returns nonzero if any case fails unless `--no-fail` is supplied.

Treat judge output as evidence, not ground truth. Inspect failed and unexpectedly easy cases, repeat borderline cases, and use human review before changing a skill boundary. The JSON annotations are the repository's intended behavior and should not be weakened merely to match a model.

For independent Codex CLI forward tests, keep each candidate session outside this repository and provide only the selected runtime files. A session started in the repository can discover its own `evals/cases.json`, expected moves, or worked example and contaminate the result. Keep judge sessions separate from candidate sessions and blind filenames when practical.

The implementation follows OpenAI's current guidance for [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs), [evaluation datasets and annotations](https://developers.openai.com/api/docs/guides/evaluation-getting-started), and [current model selection](https://developers.openai.com/api/docs/guides/latest-model.md).
