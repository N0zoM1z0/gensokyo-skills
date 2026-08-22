from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/eval_model.py"


def response_envelope(text: str, request_number: int) -> dict[str, Any]:
    return {
        "id": f"resp_test_{request_number}",
        "status": "completed",
        "model": "test-resolved-model",
        "output": [
            {
                "type": "message",
                "content": [{"type": "output_text", "text": text}],
            }
        ],
        "usage": {"input_tokens": 10, "output_tokens": 5, "total_tokens": 15},
    }


class FakeResponsesHandler(BaseHTTPRequestHandler):
    requests: list[dict[str, Any]] = []

    def do_POST(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
        length = int(self.headers["Content-Length"])
        payload = json.loads(self.rfile.read(length).decode("utf-8"))
        self.__class__.requests.append(payload)
        format_config = payload.get("text", {}).get("format", {})
        schema_name = format_config.get("name")

        if schema_name == "skill_routing":
            router_input = json.loads(payload["input"])
            selected_skill = (
                "none"
                if "one sentence in README.md" in router_input["user_request"]
                else "reimu-incident-triage"
            )
            body = {
                "selected_skill": selected_skill,
                "confidence": "high",
                "reason": (
                    "The requested machinery is disproportionate to a low-risk documentation edit."
                    if selected_skill == "none"
                    else "The request describes a noisy production regression and asks for recovery."
                ),
                "decisive_description_phrase": (
                    "low-risk implementation with no meaningful state transition"
                    if selected_skill == "none"
                    else "regressions, outages, flaky failures"
                ),
            }
        elif schema_name == "quality_judgment":
            judge_input = json.loads(payload["input"])
            a_skilled = "SKILLED" in judge_input["response_a"]

            def review(skilled: bool) -> dict[str, Any]:
                return {
                    "must_show": [
                        {"criterion": criterion, "met": skilled, "evidence": "present" if skilled else "missing"}
                        for criterion in judge_input["must_show"]
                    ],
                    "must_avoid": [
                        {"criterion": criterion, "violated": False, "evidence": "not present"}
                        for criterion in judge_input["must_avoid"]
                    ],
                    "decision_quality": 4 if skilled else 2,
                    "task_specificity": 4 if skilled else 2,
                    "total_score": 4 if skilled else 2,
                    "summary": "Skill-shaped answer." if skilled else "Generic baseline.",
                }

            body = {
                "response_a": review(a_skilled),
                "response_b": review(not a_skilled),
                "winner": "a" if a_skilled else "b",
                "distinctive_change": "The skill adds a concrete decision procedure.",
            }
        elif schema_name == "contrast_judgment":
            judge_input = json.loads(payload["input"])
            body = {
                "reviews": [
                    {
                        "skill": item["skill"],
                        "expected_move_present": True,
                        "evidence": f"The answer executes: {item['expected_move']}",
                        "decision_shape": f"Distinct decision for {item['skill']}",
                        "score": 4,
                    }
                    for item in judge_input["responses"]
                ],
                "pairwise_distinct": True,
                "collisions": [],
                "summary": "Each answer changes a different decision artifact.",
            }
        elif schema_name == "admission_judgment":
            body = {
                "deletion_test": {"passed": True, "evidence": "The stripped procedure remains executable."},
                "swap_test": {"passed": True, "evidence": "The original anchor explains the operator sequence better."},
                "operator_test": {"passed": True, "evidence": "Every operator changes an allowed state or artifact."},
                "artifact_test": {"passed": True, "evidence": "The output contract names a distinct artifact."},
                "bias_test": {"passed": True, "evidence": "The skill names its overreach and countercheck."},
                "score": 4,
                "summary": "The skill passes all admission tests.",
            }
        else:
            body = "SKILLED candidate output" if "<agent_skill>" in payload["instructions"] else "BASELINE candidate output"

        encoded = json.dumps(response_envelope(json.dumps(body) if isinstance(body, dict) else body, len(self.requests))).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, _format: str, *_args: Any) -> None:
        return


class EvalModelTests(unittest.TestCase):
    def setUp(self) -> None:
        FakeResponsesHandler.requests = []
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), FakeResponsesHandler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.api_base = f"http://127.0.0.1:{self.server.server_port}/v1"

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)

    def run_eval(self, *arguments: str) -> tuple[subprocess.CompletedProcess[str], dict[str, Any]]:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "result.json"
            environment = os.environ.copy()
            environment["OPENAI_API_KEY"] = "test-key"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "run",
                    *arguments,
                    "--api-base",
                    self.api_base,
                    "--output",
                    str(output),
                ],
                cwd=ROOT,
                env=environment,
                text=True,
                capture_output=True,
                check=False,
            )
            artifact = json.loads(output.read_text(encoding="utf-8"))
        return completed, artifact

    def test_list_all_includes_admission_cases(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), "list", "--kind", "all", "--skill", "kogasa-surprise-testing"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("admission/kogasa-surprise-testing/surprise-forge-fit", completed.stdout)

    def test_routing_uses_structured_output_and_exact_match(self) -> None:
        completed, artifact = self.run_eval(
            "--kind",
            "routing",
            "--case",
            "routing/reimu-incident-triage/trigger/1",
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(artifact["summary"]["passed"], 1)
        self.assertEqual(len(FakeResponsesHandler.requests), 1)
        request = FakeResponsesHandler.requests[0]
        self.assertFalse(request["store"])
        self.assertEqual(request["text"]["format"]["type"], "json_schema")
        self.assertTrue(request["text"]["format"]["strict"])

    def test_routing_accepts_explicit_none_near_miss(self) -> None:
        completed, artifact = self.run_eval(
            "--kind",
            "routing",
            "--case",
            "routing/sakuya-checkpointed-execution/near-miss/5",
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(artifact["summary"]["passed"], 1)
        self.assertEqual(artifact["cases"][0]["expected"], "none")
        self.assertEqual(artifact["cases"][0]["selected"], "none")

    def test_quality_runs_blinded_baseline_skill_and_judge(self) -> None:
        completed, artifact = self.run_eval(
            "--kind",
            "quality",
            "--case",
            "quality/reimu-incident-triage/",
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(artifact["summary"]["passed"], 1)
        self.assertEqual(artifact["summary"]["usage"]["total_tokens"], 45)
        self.assertEqual(len(FakeResponsesHandler.requests), 3)
        candidate_requests = [
            request for request in FakeResponsesHandler.requests if "format" not in request["text"]
        ]
        judge_requests = [
            request for request in FakeResponsesHandler.requests if request["text"].get("format", {}).get("name") == "quality_judgment"
        ]
        self.assertEqual(len(candidate_requests), 2)
        self.assertEqual(len(judge_requests), 1)
        self.assertTrue(all(request["store"] is False for request in FakeResponsesHandler.requests))
        self.assertEqual(artifact["cases"][0]["diagnostics"]["winner_condition"], "with_skill")

    def test_contrast_runs_selected_skill_pair_and_distinctness_judge(self) -> None:
        completed, artifact = self.run_eval(
            "--kind",
            "contrast",
            "--case",
            "parallel-ci",
            "--skill",
            "reimu-incident-triage",
            "--skill",
            "yukari-boundary-analysis",
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(artifact["summary"]["passed"], 1)
        self.assertEqual(len(FakeResponsesHandler.requests), 3)
        judge_requests = [
            request
            for request in FakeResponsesHandler.requests
            if request["text"].get("format", {}).get("name") == "contrast_judgment"
        ]
        self.assertEqual(len(judge_requests), 1)
        self.assertEqual(
            set(artifact["cases"][0]["diagnostics"]["skill_passes"]),
            {"reimu-incident-triage", "yukari-boundary-analysis"},
        )
        self.assertTrue(artifact["cases"][0]["judgment"]["pairwise_distinct"])

    def test_contrast_incident_can_define_a_nearest_neighbor_subset(self) -> None:
        completed, artifact = self.run_eval(
            "--kind",
            "contrast",
            "--case",
            "offline-client-key-rotation",
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(artifact["summary"]["passed"], 1)
        self.assertEqual(len(FakeResponsesHandler.requests), 4)
        self.assertEqual(
            set(artifact["cases"][0]["expected_moves"]),
            {
                "sakuya-checkpointed-execution",
                "suika-scatter-gather-planning",
                "yukari-boundary-analysis",
            },
        )

    def test_admission_strips_theme_and_runs_one_structured_judge(self) -> None:
        completed, artifact = self.run_eval(
            "--kind",
            "admission",
            "--skill",
            "kogasa-surprise-testing",
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(artifact["summary"]["passed"], 1)
        self.assertEqual(len(FakeResponsesHandler.requests), 1)
        request = FakeResponsesHandler.requests[0]
        self.assertEqual(request["text"]["format"]["name"], "admission_judgment")
        judge_input = json.loads(request["input"])
        self.assertNotIn("Kogasa", judge_input["theme_stripped_skill"])
        self.assertNotIn("Closed Umbrella", judge_input["theme_stripped_skill"])
        self.assertIn("Fix the expectation", judge_input["theme_stripped_skill"])
        self.assertEqual(
            set(artifact["cases"][0]["diagnostics"]["criterion_passes"]),
            {"deletion_test", "swap_test", "operator_test", "artifact_test", "bias_test"},
        )


if __name__ == "__main__":
    unittest.main()
