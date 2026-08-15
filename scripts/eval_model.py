#!/usr/bin/env python3
"""Run routing, baseline-quality, and cross-skill model evaluations."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import sys
import tempfile
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
DEFAULT_CONFIG = ROOT / "evals/model-config.json"
DEFAULT_API_BASE = "https://api.openai.com/v1"
RESULTS_DIR = ROOT / "eval-results"

BASELINE_INSTRUCTIONS = """You are a capable task-solving assistant. Answer the user's request directly.
Use the supplied facts, state material uncertainty, and recommend concrete next actions.
Do not mention this evaluation or claim to have performed actions you did not perform."""

SKILL_INSTRUCTIONS = """You are a capable task-solving assistant executing the Agent Skill below.
Follow its operating bias, procedure, countercheck, exit criteria, and output contract.
Treat character and spell-card language as workflow mnemonics, not a request to role-play.
Do not mention this evaluation or claim to have performed actions you did not perform.

<agent_skill>
{skill_text}
</agent_skill>"""

ROUTER_INSTRUCTIONS = """Select the single best Agent Skill for the user request from the supplied catalog.
Use only each skill's name and description. Select `none` when no description fits.
Do not select a skill merely because the user mentions its character name.
Return the required structured judgment."""

QUALITY_JUDGE_INSTRUCTIONS = """Act as a blinded evaluator of two answers to the same user request.
Evaluate semantic behavior, not exact wording. Copy every supplied criterion exactly into the matching review array.
Do not reward verbosity, character references, headings, or spell-card names by themselves.
Reward decision-relevant evidence, task specificity, safe action, and faithful coverage of the rubric.
Mark an avoid criterion violated only when the response actually exhibits it.
Return the required structured judgment and no extra commentary."""

CONTRAST_JUDGE_INSTRUCTIONS = """Evaluate whether several answers to one incident exhibit genuinely different
decision processes. For every skill, copy its id exactly, test its annotated expected move, identify its concrete
decision shape, and score execution from 0 to 4. Different vocabulary with the same plan is a collision.
Set pairwise_distinct true only when every response contributes a materially different evidence request, artifact,
scope change, decision, or stopping rule. Return the required structured judgment and no extra commentary."""


class EvalError(RuntimeError):
    """A recoverable evaluation or model response error."""


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json_atomic(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", delete=False
    ) as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
        temp_path = Path(handle.name)
    os.replace(temp_path, path)


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise EvalError("SKILL.md has no frontmatter")
    try:
        raw, _body = text[4:].split("\n---", 1)
    except ValueError as exc:
        raise EvalError("SKILL.md frontmatter is not closed") from exc
    values: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.strip():
            continue
        key, separator, value = line.partition(":")
        if not separator:
            raise EvalError(f"Unsupported frontmatter line: {line}")
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def discover_skills() -> dict[str, dict[str, Any]]:
    skills: dict[str, dict[str, Any]] = {}
    for path in sorted(SKILLS_DIR.iterdir()):
        if not path.is_dir():
            continue
        skill_path = path / "SKILL.md"
        cases_path = path / "evals/cases.json"
        if not skill_path.is_file() or not cases_path.is_file():
            continue
        skill_text = skill_path.read_text(encoding="utf-8")
        metadata = parse_frontmatter(skill_text)
        skill_id = metadata.get("name", path.name)
        skills[skill_id] = {
            "id": skill_id,
            "description": metadata.get("description", ""),
            "text": skill_text,
            "cases": read_json(cases_path),
        }
    return skills


def routing_cases(skills: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    for skill_id, skill in skills.items():
        for index, case in enumerate(skill["cases"].get("should_trigger", []), start=1):
            cases.append(
                {
                    "id": f"routing/{skill_id}/trigger/{index}",
                    "kind": "routing",
                    "prompt": case["prompt"],
                    "expected": skill_id,
                    "origin_skill": skill_id,
                    "annotation": case.get("reason", ""),
                }
            )
        for index, case in enumerate(skill["cases"].get("should_not_trigger", []), start=1):
            cases.append(
                {
                    "id": f"routing/{skill_id}/near-miss/{index}",
                    "kind": "routing",
                    "prompt": case["prompt"],
                    "expected": case.get("preferred_skill") or "none",
                    "origin_skill": skill_id,
                    "annotation": "Near-miss routing case.",
                }
            )
    return cases


def quality_cases(skills: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    for skill_id, skill in skills.items():
        for index, case in enumerate(skill["cases"].get("quality_cases", []), start=1):
            case_name = case.get("id") or str(index)
            cases.append(
                {
                    "id": f"quality/{skill_id}/{case_name}",
                    "kind": "quality",
                    "skill": skill_id,
                    "prompt": case["prompt"],
                    "must_show": case["must_show"],
                    "must_avoid": case["must_avoid"],
                }
            )
    return cases


def contrast_cases(_skills: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    data = read_json(ROOT / "evals/contrast-incidents.json")
    return [
        {
            "id": f"contrast/{case['id']}",
            "kind": "contrast",
            "prompt": case["prompt"],
            "expected_moves": case["expected_moves"],
        }
        for case in data.get("incidents", [])
    ]


def load_cases(kind: str, skills: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    if kind == "routing":
        return routing_cases(skills)
    if kind == "quality":
        return quality_cases(skills)
    if kind == "contrast":
        return contrast_cases(skills)
    return routing_cases(skills) + quality_cases(skills) + contrast_cases(skills)


def filter_cases(
    cases: list[dict[str, Any]], selectors: list[str], skill_filters: list[str], limit: int | None
) -> list[dict[str, Any]]:
    selected = cases
    if selectors:
        selected = [case for case in selected if any(selector in case["id"] for selector in selectors)]
    if skill_filters:
        wanted = set(skill_filters)
        filtered: list[dict[str, Any]] = []
        for case in selected:
            involved = {case.get("skill"), case.get("origin_skill")}
            involved.update(case.get("expected_moves", {}).keys())
            if involved & wanted:
                filtered.append(case)
        selected = filtered
    if limit is not None:
        selected = selected[:limit]
    return selected


def strict_object(properties: dict[str, Any], required: Iterable[str] | None = None) -> dict[str, Any]:
    return {
        "type": "object",
        "properties": properties,
        "required": list(required or properties.keys()),
        "additionalProperties": False,
    }


def routing_schema(skill_ids: list[str]) -> dict[str, Any]:
    return strict_object(
        {
            "selected_skill": {"type": "string", "enum": skill_ids + ["none"]},
            "confidence": {"type": "string", "enum": ["low", "medium", "high"]},
            "reason": {"type": "string"},
            "decisive_description_phrase": {"type": "string"},
        }
    )


def quality_schema() -> dict[str, Any]:
    show_item = strict_object(
        {
            "criterion": {"type": "string"},
            "met": {"type": "boolean"},
            "evidence": {"type": "string"},
        }
    )
    avoid_item = strict_object(
        {
            "criterion": {"type": "string"},
            "violated": {"type": "boolean"},
            "evidence": {"type": "string"},
        }
    )
    review = strict_object(
        {
            "must_show": {"type": "array", "items": show_item},
            "must_avoid": {"type": "array", "items": avoid_item},
            "decision_quality": {"type": "integer"},
            "task_specificity": {"type": "integer"},
            "total_score": {"type": "integer"},
            "summary": {"type": "string"},
        }
    )
    return strict_object(
        {
            "response_a": review,
            "response_b": review,
            "winner": {"type": "string", "enum": ["a", "b", "tie"]},
            "distinctive_change": {"type": "string"},
        }
    )


def contrast_schema() -> dict[str, Any]:
    review = strict_object(
        {
            "skill": {"type": "string"},
            "expected_move_present": {"type": "boolean"},
            "evidence": {"type": "string"},
            "decision_shape": {"type": "string"},
            "score": {"type": "integer"},
        }
    )
    collision = strict_object(
        {
            "skills": {"type": "array", "items": {"type": "string"}},
            "overlap": {"type": "string"},
        }
    )
    return strict_object(
        {
            "reviews": {"type": "array", "items": review},
            "pairwise_distinct": {"type": "boolean"},
            "collisions": {"type": "array", "items": collision},
            "summary": {"type": "string"},
        }
    )


def output_text(response: dict[str, Any]) -> str:
    if response.get("status") != "completed":
        details = response.get("incomplete_details") or response.get("error") or "unknown reason"
        raise EvalError(f"model response was not completed: {details}")
    chunks: list[str] = []
    for item in response.get("output", []):
        if item.get("type") != "message":
            continue
        for content in item.get("content", []):
            if content.get("type") == "refusal":
                raise EvalError(f"model refused the request: {content.get('refusal', '')}")
            if content.get("type") == "output_text":
                chunks.append(content.get("text", ""))
    if not chunks:
        raise EvalError("model response contained no output_text")
    return "\n".join(chunks)


class ResponsesClient:
    def __init__(self, api_key: str, api_base: str, timeout: int, max_retries: int) -> None:
        self.api_key = api_key
        self.url = f"{api_base.rstrip('/')}/responses"
        self.timeout = timeout
        self.max_retries = max_retries

    def create(self, payload: dict[str, Any]) -> dict[str, Any]:
        encoded = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        for attempt in range(self.max_retries + 1):
            request = urllib.request.Request(
                self.url,
                data=encoded,
                method="POST",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "User-Agent": "gensokyo-skills-eval/1",
                },
            )
            try:
                with urllib.request.urlopen(request, timeout=self.timeout) as response:
                    return json.loads(response.read().decode("utf-8"))
            except urllib.error.HTTPError as exc:
                body = exc.read().decode("utf-8", errors="replace")[:1200]
                if exc.code not in {408, 409, 429, 500, 502, 503, 504} or attempt >= self.max_retries:
                    raise EvalError(f"OpenAI API HTTP {exc.code}: {body}") from exc
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
                if attempt >= self.max_retries:
                    raise EvalError(f"OpenAI API request failed: {exc}") from exc
            time.sleep(min(2**attempt, 8))
        raise EvalError("OpenAI API retry loop ended unexpectedly")

    def generate(
        self,
        *,
        model: str,
        instructions: str,
        input_text: str,
        reasoning_effort: str,
        verbosity: str,
        max_output_tokens: int,
        metadata: dict[str, str],
        schema_name: str | None = None,
        schema: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        text_config: dict[str, Any] = {"verbosity": verbosity}
        if schema_name and schema:
            text_config["format"] = {
                "type": "json_schema",
                "name": schema_name,
                "strict": True,
                "schema": schema,
            }
        payload = {
            "model": model,
            "instructions": instructions,
            "input": input_text,
            "reasoning": {"effort": reasoning_effort},
            "text": text_config,
            "max_output_tokens": max_output_tokens,
            "store": False,
            "metadata": metadata,
        }
        response = self.create(payload)
        return {
            "id": response.get("id"),
            "requested_model": model,
            "response_model": response.get("model"),
            "status": response.get("status"),
            "usage": response.get("usage") or {},
            "text": output_text(response),
        }

    def generate_json(self, **kwargs: Any) -> tuple[dict[str, Any], dict[str, Any]]:
        result = self.generate(**kwargs)
        try:
            parsed = json.loads(result["text"])
        except json.JSONDecodeError as exc:
            raise EvalError(f"structured response was not valid JSON: {exc}") from exc
        if not isinstance(parsed, dict):
            raise EvalError("structured response root was not an object")
        return parsed, result


def deterministic_order(labels: list[str], case_id: str, seed: str) -> list[str]:
    digest = hashlib.sha256(f"{seed}:{case_id}".encode("utf-8")).digest()
    ordered = list(labels)
    random.Random(digest).shuffle(ordered)
    return ordered


def candidate_response(
    client: ResponsesClient,
    case: dict[str, Any],
    skill: dict[str, Any] | None,
    config: dict[str, Any],
) -> dict[str, Any]:
    condition = skill["id"] if skill else "baseline"
    instructions = (
        SKILL_INSTRUCTIONS.format(skill_text=skill["text"]) if skill else BASELINE_INSTRUCTIONS
    )
    return client.generate(
        model=config["candidate_model"],
        instructions=instructions,
        input_text=case["prompt"],
        reasoning_effort=config["candidate_reasoning_effort"],
        verbosity=config["candidate_verbosity"],
        max_output_tokens=config["candidate_max_output_tokens"],
        metadata={"eval_case": case["id"][:64], "eval_condition": condition[:64]},
    )


def run_routing_case(
    client: ResponsesClient, case: dict[str, Any], skills: dict[str, dict[str, Any]], config: dict[str, Any]
) -> dict[str, Any]:
    catalog = [
        {"name": skill_id, "description": skill["description"]}
        for skill_id, skill in sorted(skills.items())
    ]
    input_text = json.dumps(
        {"user_request": case["prompt"], "available_skills": catalog}, ensure_ascii=False, indent=2
    )
    judgment, response = client.generate_json(
        model=config["candidate_model"],
        instructions=ROUTER_INSTRUCTIONS,
        input_text=input_text,
        reasoning_effort=config["candidate_reasoning_effort"],
        verbosity=config["judge_verbosity"],
        max_output_tokens=1200,
        metadata={"eval_case": case["id"][:64], "eval_condition": "routing"},
        schema_name="skill_routing",
        schema=routing_schema(sorted(skills)),
    )
    selected = judgment.get("selected_skill")
    return {
        "id": case["id"],
        "kind": "routing",
        "prompt": case["prompt"],
        "expected": case["expected"],
        "selected": selected,
        "passed": selected == case["expected"],
        "judgment": judgment,
        "response": {key: value for key, value in response.items() if key != "text"},
    }


def review_criterion_map(items: Any, flag: str) -> dict[str, bool]:
    if not isinstance(items, list):
        return {}
    return {
        item.get("criterion", ""): bool(item.get(flag))
        for item in items
        if isinstance(item, dict) and item.get("criterion")
    }


def run_quality_case(
    client: ResponsesClient, case: dict[str, Any], skills: dict[str, dict[str, Any]], config: dict[str, Any]
) -> dict[str, Any]:
    skill = skills[case["skill"]]
    baseline = candidate_response(client, case, None, config)
    with_skill = candidate_response(client, case, skill, config)
    conditions = {"baseline": baseline, "with_skill": with_skill}
    order = deterministic_order(list(conditions), case["id"], config["random_seed"])
    a_condition, b_condition = order
    judge_input = json.dumps(
        {
            "user_request": case["prompt"],
            "must_show": case["must_show"],
            "must_avoid": case["must_avoid"],
            "response_a": conditions[a_condition]["text"],
            "response_b": conditions[b_condition]["text"],
        },
        ensure_ascii=False,
        indent=2,
    )
    judgment, judge_response = client.generate_json(
        model=config["judge_model"],
        instructions=QUALITY_JUDGE_INSTRUCTIONS,
        input_text=judge_input,
        reasoning_effort=config["judge_reasoning_effort"],
        verbosity=config["judge_verbosity"],
        max_output_tokens=config["judge_max_output_tokens"],
        metadata={"eval_case": case["id"][:64], "eval_condition": "quality-judge"},
        schema_name="quality_judgment",
        schema=quality_schema(),
    )

    review_by_condition = {
        a_condition: judgment.get("response_a", {}),
        b_condition: judgment.get("response_b", {}),
    }
    skill_review = review_by_condition.get("with_skill", {})
    show_map = review_criterion_map(skill_review.get("must_show"), "met")
    avoid_map = review_criterion_map(skill_review.get("must_avoid"), "violated")
    reviewed_show = skill_review.get("must_show")
    reviewed_avoid = skill_review.get("must_avoid")
    exact_show = (
        isinstance(reviewed_show, list)
        and len(reviewed_show) == len(case["must_show"])
        and set(show_map) == set(case["must_show"])
    )
    exact_avoid = (
        isinstance(reviewed_avoid, list)
        and len(reviewed_avoid) == len(case["must_avoid"])
        and set(avoid_map) == set(case["must_avoid"])
    )
    coverage = (
        sum(show_map.get(criterion, False) for criterion in case["must_show"]) / len(case["must_show"])
        if case["must_show"]
        else 1.0
    )
    violations = sum(avoid_map.get(criterion, False) for criterion in case["must_avoid"])
    score = skill_review.get("total_score", -1)
    winner_label = judgment.get("winner")
    winner_condition = {"a": a_condition, "b": b_condition, "tie": "tie"}.get(winner_label, "invalid")
    passed = (
        exact_show
        and exact_avoid
        and coverage == 1.0
        and violations == 0
        and isinstance(score, int)
        and config["quality_min_score"] <= score <= 4
        and winner_condition == "with_skill"
    )
    return {
        "id": case["id"],
        "kind": "quality",
        "skill": case["skill"],
        "prompt": case["prompt"],
        "rubric": {"must_show": case["must_show"], "must_avoid": case["must_avoid"]},
        "blind_order": {"a": a_condition, "b": b_condition},
        "outputs": conditions,
        "judgment": judgment,
        "judge_response": {key: value for key, value in judge_response.items() if key != "text"},
        "diagnostics": {
            "criterion_sets_exact": exact_show and exact_avoid,
            "must_show_coverage": coverage,
            "must_avoid_violations": violations,
            "with_skill_score": score,
            "winner_condition": winner_condition,
        },
        "passed": passed,
    }


def run_contrast_case(
    client: ResponsesClient, case: dict[str, Any], skills: dict[str, dict[str, Any]], config: dict[str, Any]
) -> dict[str, Any]:
    requested_skills = list(case["expected_moves"])
    if len(requested_skills) < 2:
        raise EvalError("contrast evaluation needs at least two skills")
    responses = {
        skill_id: candidate_response(client, case, skills[skill_id], config)
        for skill_id in requested_skills
    }
    order = deterministic_order(requested_skills, case["id"], config["random_seed"])
    judge_input = json.dumps(
        {
            "user_request": case["prompt"],
            "responses": [
                {
                    "skill": skill_id,
                    "expected_move": case["expected_moves"][skill_id],
                    "answer": responses[skill_id]["text"],
                }
                for skill_id in order
            ],
        },
        ensure_ascii=False,
        indent=2,
    )
    judgment, judge_response = client.generate_json(
        model=config["judge_model"],
        instructions=CONTRAST_JUDGE_INSTRUCTIONS,
        input_text=judge_input,
        reasoning_effort=config["judge_reasoning_effort"],
        verbosity=config["judge_verbosity"],
        max_output_tokens=config["judge_max_output_tokens"],
        metadata={"eval_case": case["id"][:64], "eval_condition": "contrast-judge"},
        schema_name="contrast_judgment",
        schema=contrast_schema(),
    )
    reviews = {
        review.get("skill"): review
        for review in judgment.get("reviews", [])
        if isinstance(review, dict) and review.get("skill")
    }
    exact_skills = (
        isinstance(judgment.get("reviews"), list)
        and len(judgment["reviews"]) == len(requested_skills)
        and set(reviews) == set(requested_skills)
    )
    skill_passes = {
        skill_id: bool(reviews.get(skill_id, {}).get("expected_move_present"))
        and isinstance(reviews.get(skill_id, {}).get("score"), int)
        and config["contrast_min_score"] <= reviews[skill_id]["score"] <= 4
        for skill_id in requested_skills
    }
    passed = exact_skills and all(skill_passes.values()) and judgment.get("pairwise_distinct") is True
    return {
        "id": case["id"],
        "kind": "contrast",
        "prompt": case["prompt"],
        "expected_moves": case["expected_moves"],
        "blind_order": order,
        "outputs": responses,
        "judgment": judgment,
        "judge_response": {key: value for key, value in judge_response.items() if key != "text"},
        "diagnostics": {"review_skill_set_exact": exact_skills, "skill_passes": skill_passes},
        "passed": passed,
    }


def count_requests(cases: list[dict[str, Any]]) -> int:
    total = 0
    for case in cases:
        if case["kind"] == "routing":
            total += 1
        elif case["kind"] == "quality":
            total += 3
        elif case["kind"] == "contrast":
            total += len(case["expected_moves"]) + 1
    return total


def usage_totals(results: list[dict[str, Any]]) -> dict[str, int]:
    totals = {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}

    def visit(value: Any) -> None:
        if isinstance(value, dict):
            usage = value.get("usage")
            if isinstance(usage, dict):
                for key in totals:
                    if isinstance(usage.get(key), int):
                        totals[key] += usage[key]
            for key, child in value.items():
                if key != "usage":
                    visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(results)
    return totals


def load_config(args: argparse.Namespace) -> dict[str, Any]:
    config = read_json(Path(args.config))
    overrides = {
        "candidate_model": args.model or os.environ.get("GK_EVAL_MODEL"),
        "judge_model": args.judge_model or os.environ.get("GK_EVAL_JUDGE_MODEL"),
        "candidate_reasoning_effort": args.reasoning_effort,
        "judge_reasoning_effort": args.judge_reasoning_effort,
    }
    for key, value in overrides.items():
        if value:
            config[key] = value
    return config


def result_path(kind: str, supplied: str | None) -> Path:
    if supplied:
        return Path(supplied)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return RESULTS_DIR / f"{stamp}-{kind}.json"


def run_command(args: argparse.Namespace, dry_run: bool) -> int:
    skills = discover_skills()
    config = load_config(args)
    cases = filter_cases(load_cases(args.kind, skills), args.case, args.skill, args.limit)
    if args.kind == "contrast" and args.skill:
        wanted = set(args.skill)
        for case in cases:
            case["expected_moves"] = {
                skill_id: move for skill_id, move in case["expected_moves"].items() if skill_id in wanted
            }
        cases = [case for case in cases if len(case["expected_moves"]) >= 2]
    if not cases:
        raise EvalError("no evaluation cases matched the requested filters")

    if dry_run:
        manifest = {
            "schema_version": 1,
            "kind": args.kind,
            "candidate_model": config["candidate_model"],
            "judge_model": config["judge_model"],
            "case_count": len(cases),
            "estimated_api_requests": count_requests(cases),
            "cases": [case["id"] for case in cases],
        }
        if args.output:
            write_json_atomic(Path(args.output), manifest)
            print(f"Wrote dry-run manifest to {args.output}")
        else:
            print(json.dumps(manifest, ensure_ascii=False, indent=2))
        return 0

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EvalError("OPENAI_API_KEY is required for live model evaluations; use dry-run without it")
    api_base = args.api_base or os.environ.get("OPENAI_BASE_URL") or DEFAULT_API_BASE
    client = ResponsesClient(
        api_key=api_key,
        api_base=api_base,
        timeout=config["request_timeout_seconds"],
        max_retries=config["max_retries"],
    )
    started = datetime.now(timezone.utc)
    results: list[dict[str, Any]] = []
    for index, case in enumerate(cases, start=1):
        print(f"[{index}/{len(cases)}] {case['id']}", file=sys.stderr)
        try:
            if case["kind"] == "routing":
                result = run_routing_case(client, case, skills, config)
            elif case["kind"] == "quality":
                result = run_quality_case(client, case, skills, config)
            else:
                result = run_contrast_case(client, case, skills, config)
        except Exception as exc:  # Keep the run artifact even when one case fails.
            result = {
                "id": case["id"],
                "kind": case["kind"],
                "passed": False,
                "error": f"{type(exc).__name__}: {exc}",
            }
        results.append(result)

    passed = sum(result.get("passed") is True for result in results)
    finished = datetime.now(timezone.utc)
    artifact = {
        "schema_version": 1,
        "run": {
            "kind": args.kind,
            "started_at": started.isoformat(),
            "finished_at": finished.isoformat(),
            "candidate_model": config["candidate_model"],
            "judge_model": config["judge_model"],
            "candidate_reasoning_effort": config["candidate_reasoning_effort"],
            "judge_reasoning_effort": config["judge_reasoning_effort"],
            "api_base": api_base,
        },
        "summary": {
            "total": len(results),
            "passed": passed,
            "failed": len(results) - passed,
            "pass_rate": passed / len(results),
            "usage": usage_totals(results),
        },
        "cases": results,
    }
    path = result_path(args.kind, args.output)
    write_json_atomic(path, artifact)
    print(f"Wrote {path}")
    print(f"Passed {passed}/{len(results)} cases")
    return 0 if passed == len(results) or args.no_fail else 1


def add_common_run_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--kind", choices=["routing", "quality", "contrast"], required=True)
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--case", action="append", default=[], help="Case-id substring; repeatable")
    parser.add_argument("--skill", action="append", default=[], help="Skill id filter; repeatable")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--model")
    parser.add_argument("--judge-model")
    parser.add_argument("--reasoning-effort", choices=["none", "low", "medium", "high", "xhigh", "max"])
    parser.add_argument("--judge-reasoning-effort", choices=["none", "low", "medium", "high", "xhigh", "max"])
    parser.add_argument("--output")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List discovered cases without calling a model")
    list_parser.add_argument("--kind", choices=["all", "routing", "quality", "contrast"], default="all")
    list_parser.add_argument("--skill", action="append", default=[])

    dry_parser = subparsers.add_parser("dry-run", help="Resolve cases and request count without calling a model")
    add_common_run_arguments(dry_parser)

    run_parser = subparsers.add_parser("run", help="Run live model evaluations through the Responses API")
    add_common_run_arguments(run_parser)
    run_parser.add_argument("--api-base", help="Responses API base URL; defaults to OPENAI_BASE_URL or OpenAI")
    run_parser.add_argument("--no-fail", action="store_true", help="Return zero even when evaluation cases fail")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "list":
            skills = discover_skills()
            cases = filter_cases(load_cases(args.kind, skills), [], args.skill, None)
            for case in cases:
                print(f"{case['id']}\t{case['prompt']}")
            print(f"{len(cases)} case(s)", file=sys.stderr)
            return 0
        return run_command(args, dry_run=args.command == "dry-run")
    except (EvalError, OSError, KeyError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
