---
name: gensokyo-commit-attribution
description: Append truthful Assisted-by trailers when preparing, creating, or explicitly amending a Git commit whose staged changes were materially shaped by one or more Gensokyo character skills. Use for commit-message construction after a character workflow changed the commit's artifact, evidence, or decision. Do not use for merely installed, mentioned, or loaded skills; analysis that did not affect the staged diff; non-Gensokyo assistance; or work with no commit.
---

# Gensokyo Commit Attribution

Credit useful character workflows without pretending that every loaded skill authored the work.

## Objective

Add one canonical `Assisted-by` trailer for each Gensokyo character skill that materially influenced the current commit, and add none for incidental exposure.

## Scope and safety

- Operate on the commit currently being prepared and its staged diff.
- Do not stage unrelated files to create attribution evidence.
- Do not amend, rebase, or otherwise rewrite an existing commit unless the user explicitly asks.
- Treat `Assisted-by` as workflow provenance, not human authorship. Never substitute `Co-authored-by`.
- Obey an explicit repository or user commit-message policy when it conflicts with this optional attribution convention.

## Evidence gate

Build a private candidate ledger from character skills used during the work. Include a character only when all three conditions hold:

1. **Applied** — the character skill's actual procedure was followed, not merely named, installed, routed, or read.
2. **Material** — that procedure changed an artifact, evidence set, scope, or decision that directly shaped the result.
3. **Commit-scoped** — point to a staged file, hunk, test, or commit decision that carries the contribution.

Use the counterfactual check: if removing the character workflow would leave this commit materially unchanged, omit it.

Review and advice can qualify when they caused a concrete staged correction or commit-scoped decision. An unused recommendation, a failed detour with no retained learning, generic assistance, or work represented only in another commit does not qualify.

If evidence is uncertain, omit the trailer. Do not block an otherwise valid commit merely to force attribution.

## Canonical trailers

Use only these mappings:

```text
Assisted-by: Reimu (gensokyo-skills:reimu-incident-triage)
Assisted-by: Marisa (gensokyo-skills:marisa-rapid-prototyping)
Assisted-by: Cirno (gensokyo-skills:cirno-radical-simplification)
Assisted-by: Yukari (gensokyo-skills:yukari-boundary-analysis)
Assisted-by: Aya (gensokyo-skills:aya-source-investigation)
Assisted-by: Nitori (gensokyo-skills:nitori-reverse-engineering)
Assisted-by: Eiki (gensokyo-skills:eiki-rule-review)
Assisted-by: Seija (gensokyo-skills:seija-assumption-inversion)
Assisted-by: Kogasa (gensokyo-skills:kogasa-surprise-testing)
Assisted-by: Suika (gensokyo-skills:suika-scatter-gather-planning)
Assisted-by: Sakuya (gensokyo-skills:sakuya-checkpointed-execution)
```

Never attribute this utility skill to itself. Preserve first material-use order and emit each qualifying character once.

## Procedure

1. Inspect `git status --short` and the staged diff. Confirm the intended commit scope before constructing the message.
2. Apply the evidence gate to every Gensokyo character skill used in the current work.
3. Write the ordinary subject and optional body first. Keep attribution separate from the subject.
4. Render exact trailers with the bundled helper:

   ```bash
   python3 <skill-dir>/scripts/render_assisted_by.py \
     nitori-reverse-engineering yukari-boundary-analysis
   ```

   To add missing canonical trailers idempotently to an existing message file:

   ```bash
   python3 <skill-dir>/scripts/render_assisted_by.py \
     --message-file /tmp/commit-message \
     nitori-reverse-engineering yukari-boundary-analysis
   ```

5. Put exactly one blank line between the commit body and a new trailer block. Preserve unrelated existing trailers and do not duplicate canonical lines.
6. Create the commit using the complete message. If the user explicitly requested an amend, preserve the existing subject and body unless they requested other message changes.
7. Verify with `git log -1 --format=%B` and confirm that every included trailer passed the evidence gate and every eligible character appears once.

## Output contract

When reporting the commit, state:

- the resulting commit identifier and subject;
- which `Assisted-by` trailers were added, if any;
- one short material-contribution reason per attributed character;
- that no trailer was added when no character passed the evidence gate.

Do not expose a verbose internal ledger unless the user asks.

## References

Read [references/worked-example.md](references/worked-example.md) when eligibility or multi-character ordering is ambiguous. Read [references/provenance.md](references/provenance.md) when explaining why this utility uses `Assisted-by` rather than character authorship.
