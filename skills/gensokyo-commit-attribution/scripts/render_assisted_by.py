#!/usr/bin/env python3
"""Render or append canonical Gensokyo Assisted-by commit trailers."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


CHARACTERS = {
    "reimu-incident-triage": "Reimu",
    "marisa-rapid-prototyping": "Marisa",
    "cirno-radical-simplification": "Cirno",
    "yukari-boundary-analysis": "Yukari",
    "aya-source-investigation": "Aya",
    "nitori-reverse-engineering": "Nitori",
    "eiki-rule-review": "Eiki",
    "seija-assumption-inversion": "Seija",
}
TRAILER_RE = re.compile(r"^[A-Za-z][A-Za-z0-9-]*:\s+\S.*$")


def canonical_trailers(skill_ids: list[str]) -> list[str]:
    """Return de-duplicated trailers in first-seen order."""

    trailers: list[str] = []
    seen: set[str] = set()
    for skill_id in skill_ids:
        if skill_id not in CHARACTERS:
            choices = ", ".join(CHARACTERS)
            raise ValueError(f"unknown character skill {skill_id!r}; choose one of: {choices}")
        if skill_id in seen:
            continue
        seen.add(skill_id)
        trailers.append(
            f"Assisted-by: {CHARACTERS[skill_id]} (gensokyo-skills:{skill_id})"
        )
    return trailers


def append_to_message(message: str, trailers: list[str]) -> str:
    """Append missing canonical lines without disturbing existing content."""

    existing = {line.strip() for line in message.splitlines()}
    missing = [line for line in trailers if line not in existing]
    if not missing:
        return message

    lines = message.splitlines()
    while lines and not lines[-1].strip():
        lines.pop()
    last_blank = max(
        (index for index, line in enumerate(lines) if not line.strip()),
        default=-1,
    )
    trailer_block = lines[last_blank + 1 :]
    has_existing_trailer_block = (
        last_blank >= 0
        and bool(trailer_block)
        and all(TRAILER_RE.fullmatch(line.strip()) for line in trailer_block)
    )
    if lines and not has_existing_trailer_block:
        lines.append("")
    lines.extend(missing)
    return "\n".join(lines) + "\n"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render canonical Assisted-by trailers for materially used Gensokyo skills."
    )
    parser.add_argument(
        "--message-file",
        type=Path,
        help="append missing trailers to this existing commit-message file",
    )
    parser.add_argument("skill", nargs="+", help="qualifying character skill id")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        trailers = canonical_trailers(args.skill)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.message_file is None:
        print("\n".join(trailers))
        return 0

    try:
        original = args.message_file.read_text(encoding="utf-8")
        updated = append_to_message(original, trailers)
        if updated != original:
            args.message_file.write_text(updated, encoding="utf-8")
    except OSError as exc:
        print(f"error: cannot update {args.message_file}: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
