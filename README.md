# Gensokyo Skills

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

These four form the v0.1 proving ground. More characters arrive only when they add a decision the existing cast cannot.

## Install

Install one self-contained skill into Codex:

```bash
git clone https://github.com/N0zoM1z0/gensokyo-skills.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R gensokyo-skills/skills/reimu-incident-triage "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Or copy any directory under `skills/` into the skills directory used by an Agent Skills-compatible client. Each runtime package contains its own `SKILL.md`, UI metadata, provenance note, worked example, and eval cases.

Invoke explicitly when you want a particular cognitive policy:

```text
Use $reimu-incident-triage to isolate this flaky CI incident.
Use $marisa-rapid-prototyping to test whether this library can handle our workload.
Use $cirno-radical-simplification to cut this design down to what the constraints earn.
Use $yukari-boundary-analysis to trace where this event contract breaks.
```

Descriptions are also written for implicit routing, with near-miss cases in each skill's `evals/cases.json`.

## Why this is more than a theme pack

Every skill must pass two deletion tests:

1. **Remove Touhou.** The remaining workflow must still be worth installing.
2. **Swap the character.** The procedure must stop making sense without substantial changes.

Every skill therefore includes:

- an activation boundary;
- a characteristic operating bias;
- concrete state-changing operators;
- a characteristic failure mode and countercheck;
- explicit exit criteria and an output contract;
- fanwork provenance kept separate from runtime guidance;
- trigger, near-miss, quality, and cross-skill contrast evals.

Read [DESIGN.md](DESIGN.md) for the full contract.

## Danmaku fingerprints

The catalog stores eight routing axes on a `0..5` scale. These are authoring signals, not claims about canon personalities.

```text
Reimu   convergence    █████   tempo          ████    simplification ████
Marisa  exploration    █████   tempo          █████   intervention   █████
Cirno   simplification █████   tempo          █████   adversarial    ████
Yukari  abstraction    █████   evidence       ████    convergence    ███
```

Fingerprints help choose contrast pairs and expose accidental overlap; native skill routing still comes from each `SKILL.md` description.

## Party composition

Use one skill by default, two when they make a real handoff, and at most three for exceptional tasks. A party is a data contract, not a meeting.

| Party | Flow | Best for |
| --- | --- | --- |
| [Hakurei Incident Duo](compositions/hakurei-incident-duo.json) | Marisa → Reimu | Experiment, then converge and recover. |
| [Border Incident Team](compositions/border-incident-team.json) | Reimu → Yukari | Bound a failure, then inspect its crossing. |
| [Frozen Boundary Review](compositions/frozen-boundary-review.json) | Cirno → Yukari | Delete machinery, then test the boundaries that remain. |

## Quality checks

Run the dependency-free repository validator:

```bash
python3 scripts/validate.py
```

The validator checks skill frontmatter, package completeness, catalog fingerprints, handoff integrity, JSON evals, reference links, and the three-member party limit. Cross-skill incidents live in [`evals/contrast-incidents.json`](evals/contrast-incidents.json); their purpose is to catch the dreaded outcome where every character becomes the same helpful chatbot.

## Repository map

```text
skills/          self-contained runtime packages
catalog/         authoring metadata and cognitive fingerprints
compositions/    small parties with explicit handoff contracts
evals/           same-incident, cross-skill contrast cases
scripts/         deterministic repository checks
```

## Contributing

Start with [CONTRIBUTING.md](CONTRIBUTING.md). A clever character mapping is welcome; a generic workflow in a funny hat is not.

Original project text and code are released under the [MIT License](LICENSE). Touhou Project and its characters belong to their respective rights holder; the license does not grant rights to third-party intellectual property.
