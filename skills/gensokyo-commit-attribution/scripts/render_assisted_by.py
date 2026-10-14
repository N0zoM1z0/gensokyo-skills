#!/usr/bin/env python3
"""Render Gensokyo assistance trailers with optional project co-author credit."""

from __future__ import annotations

import argparse
import re
import subprocess
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
    "kogasa-surprise-testing": "Kogasa",
    "suika-scatter-gather-planning": "Suika",
    "sakuya-checkpointed-execution": "Sakuya",
}
TRAILER_RE = re.compile(r"^[A-Za-z][A-Za-z0-9-]*:\s+\S.*$")
CO_AUTHOR_CONFIG = "gensokyo.coAuthor"
CO_AUTHOR_TRAILER = (
    "Co-authored-by: gensokyo-dev <342580529+gensokyo-dev@users.noreply.github.com>"
)


def canonical_trailers(skill_ids: list[str], *, co_author: bool = False) -> list[str]:
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
    if co_author and trailers:
        trailers.append(CO_AUTHOR_TRAILER)
    return trailers


def co_author_enabled(repo: Path | None = None) -> bool:
    """Read the effective Git preference; an unset preference defaults to off."""

    command = ["git"]
    if repo is not None:
        command.extend(["-C", str(repo)])
    command.extend(["config", "--bool", "--get", CO_AUTHOR_CONFIG])
    try:
        result = subprocess.run(command, text=True, capture_output=True)
    except OSError as exc:
        raise ValueError(f"cannot read {CO_AUTHOR_CONFIG}: {exc}") from exc
    if result.returncode == 1:
        return False
    if result.returncode != 0:
        raise ValueError(f"cannot read {CO_AUTHOR_CONFIG}: {result.stderr.strip()}")
    return result.stdout.strip() == "true"


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
        description="Render Assisted-by trailers with optional gensokyo-dev co-author credit."
    )
    parser.add_argument(
        "--message-file",
        type=Path,
        help="append missing trailers to this existing commit-message file",
    )
    parser.add_argument(
        "--repo",
        type=Path,
        help="read Git preferences from this repository (default: current directory)",
    )
    co_author = parser.add_mutually_exclusive_group()
    co_author.add_argument(
        "--co-author",
        dest="co_author",
        action="store_const",
        const=True,
        default=None,
        help=f"include gensokyo-dev co-author credit for this invocation, overriding {CO_AUTHOR_CONFIG}",
    )
    co_author.add_argument(
        "--no-co-author",
        dest="co_author",
        action="store_const",
        const=False,
        help=f"omit gensokyo-dev co-author credit for this invocation, overriding {CO_AUTHOR_CONFIG}",
    )
    parser.add_argument("skill", nargs="+", help="qualifying character skill id")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        co_author = (
            args.co_author
            if args.co_author is not None
            else co_author_enabled(args.repo)
        )
        trailers = canonical_trailers(args.skill, co_author=co_author)
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
