from __future__ import annotations

import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    ROOT
    / "skills"
    / "gensokyo-commit-attribution"
    / "scripts"
    / "render_assisted_by.py"
)
SPEC = importlib.util.spec_from_file_location("render_assisted_by", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class AssistedByUnitTests(unittest.TestCase):
    def test_renders_first_seen_order_and_deduplicates(self) -> None:
        self.assertEqual(
            MODULE.canonical_trailers(
                [
                    "nitori-reverse-engineering",
                    "yukari-boundary-analysis",
                    "nitori-reverse-engineering",
                ]
            ),
            [
                "Assisted-by: Nitori (gensokyo-skills:nitori-reverse-engineering)",
                "Assisted-by: Yukari (gensokyo-skills:yukari-boundary-analysis)",
            ],
        )

    def test_rejects_non_character_and_unknown_skills(self) -> None:
        for skill_id in ("gensokyo-commit-attribution", "unknown-skill"):
            with self.subTest(skill_id=skill_id), self.assertRaises(ValueError):
                MODULE.canonical_trailers([skill_id])

    def test_appends_new_block_and_is_idempotent(self) -> None:
        trailers = MODULE.canonical_trailers(
            ["nitori-reverse-engineering", "yukari-boundary-analysis"]
        )
        message = "Repair compatibility boundary\n\nExplain the retained fix.\n"
        expected = (
            "Repair compatibility boundary\n\n"
            "Explain the retained fix.\n\n"
            "Assisted-by: Nitori (gensokyo-skills:nitori-reverse-engineering)\n"
            "Assisted-by: Yukari (gensokyo-skills:yukari-boundary-analysis)\n"
        )
        updated = MODULE.append_to_message(message, trailers)
        self.assertEqual(updated, expected)
        self.assertEqual(MODULE.append_to_message(updated, trailers), updated)

    def test_preserves_existing_trailer_block(self) -> None:
        message = "Fix parser\n\nSigned-off-by: Human <human@example.com>\n"
        trailers = MODULE.canonical_trailers(["reimu-incident-triage"])
        self.assertEqual(
            MODULE.append_to_message(message, trailers),
            message + "Assisted-by: Reimu (gensokyo-skills:reimu-incident-triage)\n",
        )

    def test_subject_that_looks_like_trailer_still_gets_separator(self) -> None:
        message = "Fix: parser boundary\n"
        trailers = MODULE.canonical_trailers(["yukari-boundary-analysis"])
        self.assertEqual(
            MODULE.append_to_message(message, trailers),
            message
            + "\nAssisted-by: Yukari (gensokyo-skills:yukari-boundary-analysis)\n",
        )


class AssistedByGitIntegrationTests(unittest.TestCase):
    def run_git(self, cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", *args],
            cwd=cwd,
            check=True,
            text=True,
            capture_output=True,
        )

    def test_helper_message_survives_real_git_commit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            self.run_git(repo, "init", "--quiet")
            self.run_git(repo, "config", "user.name", "Eval User")
            self.run_git(repo, "config", "user.email", "eval@example.com")
            (repo / "parser.txt").write_text("decoded timestamp\n", encoding="utf-8")
            self.run_git(repo, "add", "parser.txt")

            message_path = repo / "message.txt"
            message_path.write_text(
                "Repair compatibility boundary\n\n"
                "Normalize the reconstructed timestamp crossing.\n",
                encoding="utf-8",
            )
            subprocess.run(
                [
                    "python3",
                    str(SCRIPT),
                    "--message-file",
                    str(message_path),
                    "nitori-reverse-engineering",
                    "yukari-boundary-analysis",
                ],
                check=True,
                text=True,
                capture_output=True,
            )
            self.run_git(repo, "commit", "--quiet", "-F", str(message_path))
            committed = self.run_git(repo, "log", "-1", "--format=%B").stdout

            self.assertIn(
                "Assisted-by: Nitori (gensokyo-skills:nitori-reverse-engineering)",
                committed,
            )
            self.assertIn(
                "Assisted-by: Yukari (gensokyo-skills:yukari-boundary-analysis)",
                committed,
            )
            self.assertEqual(committed.count("Assisted-by: Nitori"), 1)
            self.assertEqual(committed.count("Assisted-by: Yukari"), 1)


if __name__ == "__main__":
    unittest.main()
