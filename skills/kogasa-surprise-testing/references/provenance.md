# Kogasa mapping provenance

Use this note to explain the inspiration boundary, not as runtime testing guidance.

## Source anchor

The earlier *Gensokyo: Monochrome Heart* profile describes Kogasa as a forgotten karakasa-obake who seeks meaningful surprise, often fails, learns from reactions, and later demonstrates practical blacksmithing competence. See the [upstream Kogasa profile](https://github.com/N0zoM1z0/gensokyo-monochrome-heart/blob/main/design/04_characters/kogasa_tatara/skills.md).

## Interpretive bridge

This project translates those anchors into a testing policy:

1. make an expectation explicit;
2. seek a plausible condition that defeats it;
3. distinguish a genuine failure from novelty;
4. forge the discovered counterexample into a durable regression test.

This is a fan-made procedural interpretation. It is not a claim that Kogasa canonically practices software testing.

## Project-original operators

- Closed Umbrella — Fix the expectation
- Surprise Sign — Turn one expectation sideways
- Genuine Scream — Prove the smallest surprise
- Tatara Forge — Make the surprise durable
- Encore Check — Test the test

The names, procedures, output contract, and examples are original to Gensokyo Skills.

## Portrayal guardrails

- Treat surprise as violated expectation, not random chaos.
- Preserve consent, authorization, and safe execution boundaries.
- Let craft competence complete the workflow; do not reduce Kogasa to a failed joke.
- Require a real oracle so theatrical behavior does not become false bug reporting.
