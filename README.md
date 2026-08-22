# Gensokyo Skills

[![skills.sh](https://skills.sh/b/N0zoM1z0/gensokyo-skills)](https://skills.sh/N0zoM1z0/gensokyo-skills)

> An unofficial Agent Skills library that translates Touhou character motifs into distinct, testable, and composable problem-solving workflows.

**Character is policy. Spell card is operator. Skill is workflow. Incident is eval. Party is composition.**

Gensokyo Skills is built to be useful even if you have never visited Gensokyo—and recognizable if you have. The characters are not chat personas pasted over generic advice. Each skill changes how an agent gathers evidence, makes decisions, fails, and knows when to stop.

This is an unofficial fan-made project inspired by Touhou Project, created by Team Shanghai Alice. It is not official or endorsed. See [FANWORK_NOTICE.md](FANWORK_NOTICE.md).

## Something strange is happening. Who do you call?

| Incident report | Caller | Skill | Signature move |
| --- | --- | --- | --- |
| “Five symptoms appeared after one deploy.” | Reimu / 博麗霊夢 | [`reimu-incident-triage`](skills/reimu-incident-triage/) | Converge on the real abnormality and restore normality. |
| “We need evidence before choosing this approach.” | Marisa / 霧雨魔理沙 | [`marisa-rapid-prototyping`](skills/marisa-rapid-prototyping/) | Borrow, build the smallest experiment, run, learn. |
| “Our tiny app has become an infrastructure summit.” | Cirno / チルノ | [`cirno-radical-simplification`](skills/cirno-radical-simplification/) | Freeze scope, use three parts, make complexity earn its return. |
| “Both components work alone; together they fail.” | Yukari / 八雲紫 | [`yukari-boundary-analysis`](skills/yukari-boundary-analysis/) | Map the crossing, trace one traveler, repair the contract. |
| “Everyone repeats the claim, but where did it come from?” | Aya / 射命丸文 | [`aya-source-investigation`](skills/aya-source-investigation/) | Split the claim, climb to primary evidence, expose circular reporting. |
| “The artifact works, but nobody knows how.” | Nitori / 河城にとり | [`nitori-reverse-engineering`](skills/nitori-reverse-engineering/) | Preserve, probe one variable, reconstruct, predict. |
| “Which rule applies, and what remedy is proportionate?” | Eiki / 四季映姫 | [`eiki-rule-review`](skills/eiki-rule-review/) | Establish authority, weigh testimony, judge each element, leave a correction path. |
| “What if the premise everyone protects is backwards?” | Seija / 鬼人正邪 | [`seija-assumption-inversion`](skills/seija-assumption-inversion/) | Invert one load-bearing assumption and follow the fallout. |
| “The happy path passes. What plausible surprise would break its promise?” | Kogasa / 多々良小傘 | [`kogasa-surprise-testing`](skills/kogasa-surprise-testing/) | Expose one genuine counterexample and forge it into a regression guard. |
| “Several agents can help, but their work still has to merge.” | Suika / 伊吹萃香 | [`suika-scatter-gather-planning`](skills/suika-scatter-gather-planning/) | Define the whole, scatter across honest seams, gather through a merge contract. |
| “This live change needs checkpoints, gates, and a rollback we can actually trust.” | Sakuya / 十六夜咲夜 | [`sakuya-checkpointed-execution`](skills/sakuya-checkpointed-execution/) | Sequence state transitions, admit irreversibility, verify every interval. |

The first four established the design language. The second wave added sourcing, mechanism reconstruction, rule-governed judgment, and adversarial reframing. The third adds counterexample-to-regression testing, parallel work recombination, and checkpointed execution. More characters still arrive only when they add a decision the existing cast cannot.

## Install

### Agent Skills CLI

The recommended cross-agent route uses the npm-delivered [`skills` CLI](https://github.com/vercel-labs/skills). The skills themselves are fetched from this GitHub repository; there is no separate `gensokyo-skills` npm package to install. The current CLI requires Node.js 22.20 or newer.

Browse the indexed collection on [skills.sh](https://skills.sh/N0zoM1z0/gensokyo-skills). The public page can lag a newly merged release briefly; the CLI command below is the direct discovery check against the repository's current default branch.

Inspect all available skills without installing:

```bash
npx skills add N0zoM1z0/gensokyo-skills --list
```

Install interactively to any detected supported agent:

```bash
npx skills add N0zoM1z0/gensokyo-skills
```

Install one skill globally for Codex without prompts:

```bash
npx skills add N0zoM1z0/gensokyo-skills \
  --skill reimu-incident-triage \
  --agent codex \
  --global \
  --yes
```

Replace the skill name with another caller, or use `--skill '*'` to install the whole roster. To try one workflow without installing it:

```bash
npx skills use N0zoM1z0/gensokyo-skills@reimu-incident-triage
```

Refresh globally installed skills later with:

```bash
npx skills update --global
```

### ChatGPT and Codex plugin

The repository root is also a skills-only OpenAI plugin. Add its Git-backed marketplace, then install the bundle:

```bash
codex plugin marketplace add N0zoM1z0/gensokyo-skills
codex plugin add gensokyo-skills@gensokyo-skills
```

Start a new thread after installation so the eleven character workflows and commit-attribution utility are available. Upgrade the marketplace snapshot later with `codex plugin marketplace upgrade gensokyo-skills`.

Each runtime package contains its own `SKILL.md`, UI metadata, provenance note, worked example, and eval cases. Manual copying remains possible, but the commands above preserve source tracking and update workflows.

Invoke explicitly when you want a particular cognitive policy:

```text
Use $reimu-incident-triage to isolate this flaky CI incident.
Use $marisa-rapid-prototyping to test whether this library can handle our workload.
Use $cirno-radical-simplification to cut this design down to what the constraints earn.
Use $yukari-boundary-analysis to trace where this event contract breaks.
Use $aya-source-investigation to verify whether these articles share one weak source.
Use $nitori-reverse-engineering to infer this binary format from controlled samples.
Use $eiki-rule-review to review this action against the governing policy.
Use $seija-assumption-inversion to reverse the premise holding this design in place.
Use $kogasa-surprise-testing to turn one contract-breaking surprise into a regression test.
Use $suika-scatter-gather-planning to split this deliverable into mergeable work packets.
Use $sakuya-checkpointed-execution to write a gated runbook for this risky state transition.
Use $gensokyo-commit-attribution when these workflows materially shaped a commit.
```

Descriptions are also written for implicit routing, with near-miss cases in each skill's `evals/cases.json`.

## Leave a trace in the spell history

When one or more character workflows actually change a committed artifact, evidence set, scope, or decision, [`gensokyo-commit-attribution`](skills/gensokyo-commit-attribution/) can add truthful Git trailers:

```text
Repair timestamp compatibility boundary

Assisted-by: Nitori (gensokyo-skills:nitori-reverse-engineering)
Assisted-by: Yukari (gensokyo-skills:yukari-boundary-analysis)
```

The utility recognizes all eleven character skills, including Kogasa, Suika, and Sakuya. It is deliberately strict: installing, mentioning, or merely loading a skill earns no attribution. A character must have been applied, materially useful, and represented in the staged commit. `Assisted-by` records workflow provenance; it does not claim human or co-author status.

## Why this is more than a theme pack

Every character skill must pass two deletion tests:

1. **Remove Touhou.** The remaining workflow must still be worth installing.
2. **Swap the character.** The procedure must stop making sense without substantial changes.

Every character skill therefore includes:

- an activation boundary;
- a characteristic operating bias;
- concrete state-changing operators;
- a characteristic failure mode and countercheck;
- explicit exit criteria and an output contract;
- fanwork provenance kept separate from runtime guidance;
- trigger, near-miss, quality, and cross-skill contrast evals.

Read [DESIGN.md](DESIGN.md) for the full contract.

## Danmaku fingerprints

The character catalog stores eight routing axes on a `0..5` scale. These are authoring signals, not claims about canon personalities. Utility workflows such as commit attribution are cataloged separately and do not receive fictional character fingerprints.

```text
Reimu   convergence    █████   tempo          ████    simplification ████
Marisa  exploration    █████   tempo          █████   intervention   █████
Cirno   simplification █████   tempo          █████   adversarial    ████
Yukari  abstraction    █████   evidence       ████    convergence    ███
Aya     evidence       █████   tempo          █████   exploration    ████
Nitori  exploration    ████    evidence       ████    intervention   ████
Eiki    evidence       █████   convergence    █████   adversarial    ███
Seija   adversarial    █████   exploration    █████   abstraction    ████
Kogasa  evidence       █████   intervention   █████   adversarial    ████
Suika   convergence    ████    tempo          ████    abstraction    ███
Sakuya  convergence    █████   evidence       █████   intervention   ████
```

Fingerprints help choose contrast pairs and expose accidental overlap; native skill routing still comes from each `SKILL.md` description.

## Party composition

Use one skill by default, two when they make a real handoff, and at most three for exceptional tasks. A party is a data contract, not a meeting.

| Party | Flow | Best for |
| --- | --- | --- |
| [Hakurei Incident Duo](compositions/hakurei-incident-duo.json) | Marisa → Reimu | Experiment, then converge and recover. |
| [Border Incident Team](compositions/border-incident-team.json) | Reimu → Yukari | Bound a failure, then inspect its crossing. |
| [Frozen Boundary Review](compositions/frozen-boundary-review.json) | Cirno → Yukari | Delete machinery, then test the boundaries that remain. |
| [Tengu–Kappa Investigation](compositions/tengu-kappa-investigation.json) | Aya → Nitori | Verify the external claim, then reconstruct the mechanism. |
| [Yama–Rebel Review](compositions/yama-rebel-review.json) | Eiki → Seija | Establish the governing rule, then pressure-test its hidden premise. |
| [Kappa Border Lab](compositions/kappa-border-lab.json) | Yukari → Nitori | Locate the failing crossing, then infer the mechanism behind it. |

## Quality checks

Run the dependency-free repository validator:

```bash
python3 scripts/validate.py
```

The validator checks skill frontmatter, package completeness, catalog fingerprints, handoff integrity, JSON evals, reference links, and the three-member party limit. Cross-skill incidents live in [`evals/contrast-incidents.json`](evals/contrast-incidents.json); their purpose is to catch the dreaded outcome where every character becomes the same helpful chatbot.

Then inspect or run the model eval suite:

```bash
python3 scripts/eval_model.py list --kind all
python3 scripts/eval_model.py dry-run --kind quality
python3 scripts/eval_model.py dry-run --kind admission --skill kogasa-surprise-testing
# With OPENAI_API_KEY set:
python3 scripts/eval_model.py run --kind routing
```

The runner uses structured judgments, keeps API storage disabled, records token usage and resolved model names, and writes inspectable run artifacts under ignored `eval-results/`. See [EVALS.md](EVALS.md) for the rubric and cost-aware commands.

## Repository map

```text
.codex-plugin/   OpenAI skills-only plugin manifest
.agents/plugins/ Git-backed Codex plugin marketplace
skills/          self-contained runtime packages
catalog/         authoring metadata and cognitive fingerprints
compositions/    small parties with explicit handoff contracts
evals/           same-incident, cross-skill contrast cases
scripts/         deterministic checks and the model eval runner
tests/           offline Responses API contract tests
```

## Contributing

Start with [CONTRIBUTING.md](CONTRIBUTING.md). A clever character mapping is welcome; a generic workflow in a funny hat is not.

Original project text and code are released under the [MIT License](LICENSE). Touhou Project and its characters belong to their respective rights holder; the license does not grant rights to third-party intellectual property.
