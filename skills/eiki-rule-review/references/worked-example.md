# Worked example: a secret appears in logs

## Input

> A developer accidentally logged an API credential. Our policy forbids exposing secrets. Should they lose production access permanently?

## Scope and authority

Use the current credential-handling and incident-response policies. Confirm whether accidental logging, storage duration, access scope, and post-incident duties are separate elements.

## Record

- Fact: one credential appeared in an internal log for twelve minutes.
- Fact: the developer reported it and the credential was rotated.
- Unknown: whether anyone accessed the value.
- Context: the logging library made sensitive-field filtering optional and no test enforced it.

## Element review

The secret-exposure rule was violated. Deliberate disclosure is not established. Required notification and rotation were completed.

## Severity and remedy

Treat the exposure as material because the credential was usable, with mitigation for short duration, prompt reporting, and no known exploitation. Permanent access removal is not tied to recurrence or current risk.

Recommend a time-bounded review, secret scanning, mandatory log redaction, a regression test, and verification that the credential is unusable. Escalate only if evidence shows concealment, misuse, or repeated disregard.

## Why this is Eiki-shaped

The workflow reaches a clear violation judgment but separates action, intent, consequence, and correction before choosing a proportionate remedy.
