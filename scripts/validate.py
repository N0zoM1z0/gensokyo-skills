#!/usr/bin/env python3
"""Validate Gensokyo Skills packages and authoring metadata."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONTMATTER_RE = re.compile(r"\A---\n(?P<body>.*?)\n---(?:\n|\Z)", re.DOTALL)
REFERENCE_LINK_RE = re.compile(r"\[[^\]]+\]\((references/[^)#]+)(?:#[^)]+)?\)")
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
EXPECTED_PACKAGE_FILES = (
    "SKILL.md",
    "agents/openai.yaml",
    "references/provenance.md",
    "references/worked-example.md",
    "evals/cases.json",
)


class Validation:
    def __init__(self) -> None:
        self.errors: list[str] = []

    def check(self, condition: bool, message: str) -> None:
        if not condition:
            self.errors.append(message)

    def load_json(self, path: Path) -> Any:
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            self.errors.append(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")
            return None


def parse_frontmatter(path: Path, validation: Validation) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        validation.errors.append(f"{path.relative_to(ROOT)}: missing YAML frontmatter")
        return {}

    values: dict[str, str] = {}
    for line in match.group("body").splitlines():
        if not line.strip():
            continue
        if ":" not in line or line.startswith((" ", "\t")):
            validation.errors.append(
                f"{path.relative_to(ROOT)}: frontmatter must use one-line scalar values"
            )
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def validate_skill(
    path: Path, skill_ids: set[str], validation: Validation
) -> tuple[int, int]:
    skill_id = path.name
    validation.check(bool(SLUG_RE.fullmatch(skill_id)), f"skills/{skill_id}: invalid slug")

    for relative in EXPECTED_PACKAGE_FILES:
        validation.check((path / relative).is_file(), f"skills/{skill_id}: missing {relative}")

    skill_md = path / "SKILL.md"
    if not skill_md.is_file():
        return 0, 0

    text = skill_md.read_text(encoding="utf-8")
    values = parse_frontmatter(skill_md, validation)
    validation.check(
        set(values) == {"name", "description"},
        f"skills/{skill_id}/SKILL.md: frontmatter keys must be exactly name and description",
    )
    validation.check(values.get("name") == skill_id, f"skills/{skill_id}: name must match directory")
    validation.check(
        len(values.get("description", "")) >= 80,
        f"skills/{skill_id}: description is too short for reliable routing",
    )
    validation.check("Use for" in values.get("description", ""), f"skills/{skill_id}: description needs positive trigger language")
    validation.check("Do not use" in values.get("description", ""), f"skills/{skill_id}: description needs a negative routing boundary")
    validation.check("TODO" not in text, f"skills/{skill_id}/SKILL.md: unresolved TODO")

    for relative in REFERENCE_LINK_RE.findall(text):
        validation.check((path / relative).is_file(), f"skills/{skill_id}: broken link {relative}")

    agent_yaml = path / "agents/openai.yaml"
    if agent_yaml.is_file():
        agent_text = agent_yaml.read_text(encoding="utf-8")
        validation.check(
            f"${skill_id}" in agent_text,
            f"skills/{skill_id}/agents/openai.yaml: default prompt must mention ${skill_id}",
        )
        validation.check("TODO" not in agent_text, f"skills/{skill_id}/agents/openai.yaml: unresolved TODO")

    eval_path = path / "evals/cases.json"
    routing_count = 0
    quality_count = 0
    if eval_path.is_file():
        cases = validation.load_json(eval_path)
        if isinstance(cases, dict):
            validation.check(cases.get("skill") == skill_id, f"skills/{skill_id}: eval skill id mismatch")
            triggers = cases.get("should_trigger", [])
            near_misses = cases.get("should_not_trigger", [])
            quality_cases = cases.get("quality_cases", [])
            validation.check(isinstance(triggers, list), f"skills/{skill_id}: should_trigger must be an array")
            validation.check(isinstance(near_misses, list), f"skills/{skill_id}: should_not_trigger must be an array")
            validation.check(isinstance(quality_cases, list), f"skills/{skill_id}: quality_cases must be an array")
            if not isinstance(triggers, list) or not isinstance(near_misses, list) or not isinstance(quality_cases, list):
                return 0, 0
            routing_count = len(triggers) + len(near_misses)
            quality_count = len(quality_cases)
            validation.check(len(triggers) >= 3, f"skills/{skill_id}: need at least three should-trigger cases")
            validation.check(len(near_misses) >= 3, f"skills/{skill_id}: need at least three near-miss cases")
            validation.check(bool(quality_cases), f"skills/{skill_id}: need at least one quality case")
            for index, case in enumerate(triggers, start=1):
                validation.check(isinstance(case, dict), f"skills/{skill_id}: trigger {index} must be an object")
                if isinstance(case, dict):
                    validation.check(bool(case.get("prompt")), f"skills/{skill_id}: trigger {index} needs a prompt")
                    validation.check(bool(case.get("reason")), f"skills/{skill_id}: trigger {index} needs a reason")
            for index, case in enumerate(near_misses, start=1):
                validation.check(isinstance(case, dict), f"skills/{skill_id}: near-miss {index} must be an object")
                if not isinstance(case, dict):
                    continue
                validation.check(bool(case.get("prompt")), f"skills/{skill_id}: near-miss {index} needs a prompt")
                preferred = case.get("preferred_skill")
                validation.check(
                    preferred is None or preferred in skill_ids,
                    f"skills/{skill_id}: near-miss {index} has unknown preferred_skill {preferred}",
                )
                validation.check(
                    preferred != skill_id,
                    f"skills/{skill_id}: near-miss {index} cannot prefer its own skill",
                )
            quality_ids: list[str] = []
            for index, case in enumerate(quality_cases, start=1):
                validation.check(isinstance(case, dict), f"skills/{skill_id}: quality case {index} must be an object")
                if not isinstance(case, dict):
                    continue
                case_id = case.get("id")
                quality_ids.append(case_id if isinstance(case_id, str) else "")
                validation.check(
                    isinstance(case_id, str) and bool(SLUG_RE.fullmatch(case_id)),
                    f"skills/{skill_id}: quality case {index} needs a stable slug id",
                )
                validation.check(bool(case.get("prompt")), f"skills/{skill_id}: quality case {case_id or index} needs a prompt")
                must_show = case.get("must_show", [])
                must_avoid = case.get("must_avoid", [])
                validation.check(
                    isinstance(must_show, list) and len(must_show) >= 3 and all(isinstance(item, str) and item for item in must_show),
                    f"skills/{skill_id}: quality case {case_id or index} needs at least three must_show strings",
                )
                validation.check(
                    isinstance(must_avoid, list) and len(must_avoid) >= 1 and all(isinstance(item, str) and item for item in must_avoid),
                    f"skills/{skill_id}: quality case {case_id or index} needs at least one must_avoid string",
                )
                if isinstance(must_show, list):
                    validation.check(len(must_show) == len(set(must_show)), f"skills/{skill_id}: duplicate must_show criterion")
                if isinstance(must_avoid, list):
                    validation.check(len(must_avoid) == len(set(must_avoid)), f"skills/{skill_id}: duplicate must_avoid criterion")
            validation.check(len(quality_ids) == len(set(quality_ids)), f"skills/{skill_id}: duplicate quality case ids")
    return routing_count, quality_count


def validate_model_config(validation: Validation) -> None:
    path = ROOT / "evals/model-config.json"
    config = validation.load_json(path)
    if not isinstance(config, dict):
        return
    validation.check(config.get("schema_version") == 1, "evals/model-config.json: schema_version must be 1")
    for key in ("candidate_model", "judge_model", "random_seed"):
        validation.check(isinstance(config.get(key), str) and bool(config[key]), f"evals/model-config.json: {key} must be a non-empty string")
    for key in ("candidate_reasoning_effort", "judge_reasoning_effort"):
        validation.check(
            config.get(key) in {"none", "low", "medium", "high", "xhigh", "max"},
            f"evals/model-config.json: invalid {key}",
        )
    for key in ("candidate_verbosity", "judge_verbosity"):
        validation.check(config.get(key) in {"low", "medium", "high"}, f"evals/model-config.json: invalid {key}")
    for key in ("candidate_max_output_tokens", "judge_max_output_tokens", "request_timeout_seconds"):
        validation.check(isinstance(config.get(key), int) and config[key] > 0, f"evals/model-config.json: {key} must be positive")
    validation.check(isinstance(config.get("max_retries"), int) and config["max_retries"] >= 0, "evals/model-config.json: max_retries must be nonnegative")
    for key in ("quality_min_score", "contrast_min_score"):
        validation.check(isinstance(config.get(key), int) and 0 <= config[key] <= 4, f"evals/model-config.json: {key} must be in 0..4")


def validate_catalog(skill_ids: set[str], validation: Validation) -> None:
    path = ROOT / "catalog/skills.json"
    catalog = validation.load_json(path)
    if not isinstance(catalog, dict):
        return

    axes = catalog.get("fingerprint_axes", [])
    entries = catalog.get("skills", [])
    catalog_ids = [entry.get("id") for entry in entries if isinstance(entry, dict)]
    validation.check(len(catalog_ids) == len(set(catalog_ids)), "catalog/skills.json: duplicate skill ids")
    validation.check(set(catalog_ids) == skill_ids, "catalog/skills.json: entries must match skill directories")

    for entry in entries:
        if not isinstance(entry, dict):
            validation.errors.append("catalog/skills.json: each skill entry must be an object")
            continue
        skill_id = entry.get("id", "<unknown>")
        fingerprint = entry.get("fingerprint", {})
        validation.check(set(fingerprint) == set(axes), f"catalog: {skill_id} fingerprint axes mismatch")
        for axis, value in fingerprint.items():
            validation.check(
                isinstance(value, int) and 0 <= value <= 5,
                f"catalog: {skill_id}.{axis} must be an integer from 0 to 5",
            )
        for field in ("signature_strength", "failure_mode", "countercheck", "operators"):
            validation.check(bool(entry.get(field)), f"catalog: {skill_id} missing {field}")


def validate_compositions(skill_ids: set[str], validation: Validation) -> int:
    count = 0
    for path in sorted((ROOT / "compositions").glob("*.json")):
        count += 1
        composition = validation.load_json(path)
        if not isinstance(composition, dict):
            continue
        members = composition.get("members", [])
        member_ids = [member.get("skill") for member in members if isinstance(member, dict)]
        validation.check(1 < len(member_ids) <= 3, f"{path.relative_to(ROOT)}: party size must be 2 or 3")
        validation.check(len(member_ids) == len(set(member_ids)), f"{path.relative_to(ROOT)}: duplicate party member")
        for skill_id in member_ids:
            validation.check(skill_id in skill_ids, f"{path.relative_to(ROOT)}: unknown skill {skill_id}")
        validation.check(bool(composition.get("sequence")), f"{path.relative_to(ROOT)}: missing sequence")
        validation.check(bool(composition.get("handoffs")), f"{path.relative_to(ROOT)}: missing handoff")
        for handoff in composition.get("handoffs", []):
            if not isinstance(handoff, dict):
                validation.errors.append(f"{path.relative_to(ROOT)}: invalid handoff")
                continue
            validation.check(handoff.get("from") in member_ids, f"{path.relative_to(ROOT)}: handoff sender is not a member")
            validation.check(handoff.get("to") in member_ids, f"{path.relative_to(ROOT)}: handoff receiver is not a member")
            validation.check(bool(handoff.get("provides")), f"{path.relative_to(ROOT)}: handoff needs provides")
            validation.check(bool(handoff.get("expects")), f"{path.relative_to(ROOT)}: handoff needs expects")
    return count


def validate_contrast(skill_ids: set[str], validation: Validation) -> int:
    path = ROOT / "evals/contrast-incidents.json"
    data = validation.load_json(path)
    if not isinstance(data, dict):
        return 0
    incidents = data.get("incidents", [])
    validation.check(len(incidents) >= 4, "evals/contrast-incidents.json: need at least four incidents")
    incident_ids = [incident.get("id") for incident in incidents if isinstance(incident, dict)]
    validation.check(len(incident_ids) == len(set(incident_ids)), "evals/contrast-incidents.json: duplicate incident ids")
    for incident in incidents:
        if not isinstance(incident, dict):
            validation.errors.append("evals/contrast-incidents.json: incident must be an object")
            continue
        expected = incident.get("expected_moves", {})
        validation.check(
            isinstance(incident.get("id"), str) and bool(SLUG_RE.fullmatch(incident["id"])),
            "evals/contrast-incidents.json: every incident needs a stable slug id",
        )
        validation.check(bool(incident.get("prompt")), f"contrast incident {incident.get('id', '<unknown>')}: missing prompt")
        validation.check(
            set(expected) == skill_ids,
            f"contrast incident {incident.get('id', '<unknown>')}: expected moves must cover every skill",
        )
        validation.check(len(set(expected.values())) == len(expected), f"contrast incident {incident.get('id', '<unknown>')}: expected moves must be distinct")
    return len(incidents)


def validate_markdown_links(validation: Validation) -> None:
    for path in ROOT.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for target in MARKDOWN_LINK_RE.findall(text):
            target = target.split("#", 1)[0]
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            validation.check(
                (path.parent / target).resolve().exists(),
                f"{path.relative_to(ROOT)}: broken local link {target}",
            )


def main() -> int:
    validation = Validation()
    skill_paths = sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir())
    skill_ids = {path.name for path in skill_paths}
    validation.check(bool(skill_paths), "skills/: no skill packages found")

    routing_count = 0
    quality_count = 0
    for path in skill_paths:
        skill_routing_count, skill_quality_count = validate_skill(path, skill_ids, validation)
        routing_count += skill_routing_count
        quality_count += skill_quality_count
    validate_catalog(skill_ids, validation)
    validate_model_config(validation)
    composition_count = validate_compositions(skill_ids, validation)
    contrast_count = validate_contrast(skill_ids, validation)
    validate_markdown_links(validation)

    for json_path in ROOT.rglob("*.json"):
        validation.load_json(json_path)

    if validation.errors:
        print(f"Validation failed with {len(validation.errors)} error(s):", file=sys.stderr)
        for error in validation.errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        f"Validated {len(skill_paths)} skills, {composition_count} compositions, "
        f"{routing_count} routing cases, {quality_count} quality cases, "
        f"and {contrast_count} contrast incidents."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
