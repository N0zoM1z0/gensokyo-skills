# Worked example: a repaired compatibility boundary

## Situation

Nitori's workflow reconstructed an undocumented timestamp field from controlled samples. Yukari's workflow then traced a UTC/local-time conversion mismatch across the parser–API boundary. The staged diff contains the inferred parser rule, a boundary normalization fix, and regression tests for both.

Aya was also loaded to inspect an external blog post, but that post was not used after primary samples contradicted it. Reimu suggested a rollback early in the investigation, but no rollback decision or artifact appears in this commit.

## Evidence gate

| Candidate | Applied | Material | Commit-scoped | Result |
| --- | --- | --- | --- | --- |
| Nitori | Controlled differential samples produced the field model. | The model determined parser behavior. | Parser and format tests retain it. | Include. |
| Yukari | One timestamp was traced across the representation boundary. | The trace identified the normalization fix. | API adapter and regression test retain it. | Include. |
| Aya | The source workflow began but its evidence was rejected. | No retained decision depends on it. | No staged artifact carries it. | Omit. |
| Reimu | A recovery option was mentioned but not executed. | It did not shape this change. | Nothing staged represents it. | Omit. |

## Commit message

```text
Repair timestamp compatibility boundary

Normalize decoded timestamps at the parser–API crossing and cover the inferred legacy field layout.

Assisted-by: Nitori (gensokyo-skills:nitori-reverse-engineering)
Assisted-by: Yukari (gensokyo-skills:yukari-boundary-analysis)
```

The order follows first material contribution. Re-running the helper with either skill does not duplicate its canonical line.
