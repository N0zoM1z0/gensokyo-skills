from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
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
PROJECT_CREDIT = (
    "Co-authored-by: gensokyo-dev <342580529+gensokyo-dev@users.noreply.github.com>"
)


class AssistedByUnitTests(unittest.TestCase):
    def test_opt_in_preserves_character_credit_and_adds_project_once(self) -> None:
        self.assertEqual(
            MODULE.canonical_trailers(
                [
                    "nitori-reverse-engineering",
                    "yukari-boundary-analysis",
                    "nitori-reverse-engineering",
                ],
                co_author=True,
            ),
            [
                "Assisted-by: Nitori (gensokyo-skills:nitori-reverse-engineering)",
                "Assisted-by: Yukari (gensokyo-skills:yukari-boundary-analysis)",
                PROJECT_CREDIT,
            ],
        )

    def test_no_project_credit_without_a_qualifying_character(self) -> None:
        self.assertEqual(MODULE.canonical_trailers([], co_author=True), [])
        with self.assertRaises(ValueError):
            MODULE.canonical_trailers(["gensokyo-commit-attribution"], co_author=True)

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

    def test_renders_third_wave_characters(self) -> None:
        self.assertEqual(
            MODULE.canonical_trailers(
                [
                    "kogasa-surprise-testing",
                    "suika-scatter-gather-planning",
                    "sakuya-checkpointed-execution",
                ]
            ),
            [
                "Assisted-by: Kogasa (gensokyo-skills:kogasa-surprise-testing)",
                "Assisted-by: Suika (gensokyo-skills:suika-scatter-gather-planning)",
                "Assisted-by: Sakuya (gensokyo-skills:sakuya-checkpointed-execution)",
            ],
        )

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
    def setUp(self) -> None:
        config_directory = tempfile.TemporaryDirectory()
        self.addCleanup(config_directory.cleanup)
        self.env = {
            key: value for key, value in os.environ.items() if not key.startswith("GIT_")
        }
        self.env["GIT_CONFIG_NOSYSTEM"] = "1"
        self.env["GIT_CONFIG_GLOBAL"] = str(Path(config_directory.name) / "gitconfig")

    def run_git(self, cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", *args],
            cwd=cwd,
            env=self.env,
            check=True,
            text=True,
            capture_output=True,
        )

    def run_helper(
        self, cwd: Path, *args: str, check: bool = True
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            cwd=cwd,
            env=self.env,
            check=check,
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
            self.run_helper(
                repo,
                "--message-file",
                str(message_path),
                "nitori-reverse-engineering",
                "yukari-boundary-analysis",
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
            self.assertNotIn("Co-authored-by:", committed)

    def test_git_preferences_and_single_use_overrides(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            self.run_git(repo, "init", "--quiet")

            def assert_credit(expected: bool, *flags: str) -> None:
                output = self.run_helper(repo, *flags, "reimu-incident-triage").stdout
                self.assertIn("Assisted-by: Reimu", output)
                self.assertEqual(PROJECT_CREDIT in output, expected)

            assert_credit(False)
            assert_credit(True, "--co-author")
            assert_credit(False)
            self.run_git(repo, "config", "--global", "gensokyo.coAuthor", "true")
            assert_credit(True)
            assert_credit(False, "--no-co-author")
            assert_credit(True)
            self.run_git(repo, "config", "--local", "gensokyo.coAuthor", "false")
            assert_credit(False)
            assert_credit(True, "--co-author")
            assert_credit(False)
            self.run_git(repo, "config", "--global", "gensokyo.coAuthor", "false")
            self.run_git(repo, "config", "--local", "gensokyo.coAuthor", "true")
            assert_credit(True)
            assert_credit(False, "--no-co-author")
            assert_credit(True)

    def test_repo_option_reads_the_target_repository(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            outside = Path(directory)
            repo = outside / "target"
            repo.mkdir()
            self.run_git(repo, "init", "--quiet")
            self.run_git(repo, "config", "gensokyo.coAuthor", "true")
            output = self.run_helper(
                outside, "--repo", str(repo), "reimu-incident-triage"
            ).stdout
            self.assertIn(PROJECT_CREDIT, output)
            self.run_git(repo, "config", "gensokyo.coAuthor", "false")
            output = self.run_helper(
                outside, "--repo", str(repo), "reimu-incident-triage"
            ).stdout
            self.assertNotIn(PROJECT_CREDIT, output)

    def test_invalid_preference_leaves_message_unchanged(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            self.run_git(repo, "init", "--quiet")
            self.run_git(repo, "config", "gensokyo.coAuthor", "invalid")
            message_path = repo / "message.txt"
            original = "Repair parser\n\nKeep this body.\n"
            message_path.write_text(original, encoding="utf-8")
            result = self.run_helper(
                repo,
                "--message-file",
                str(message_path),
                "nitori-reverse-engineering",
                check=False,
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("gensokyo.coAuthor", result.stderr)
            self.assertEqual(message_path.read_text(encoding="utf-8"), original)
            for flag, expected_credit in (("--co-author", True), ("--no-co-author", False)):
                with self.subTest(flag=flag):
                    result = self.run_helper(repo, flag, "nitori-reverse-engineering")
                    self.assertEqual(PROJECT_CREDIT in result.stdout, expected_credit)

    def test_opted_in_message_is_idempotent_and_survives_git_commit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            self.run_git(repo, "init", "--quiet")
            self.run_git(repo, "config", "user.name", "Eval User")
            self.run_git(repo, "config", "user.email", "eval@example.com")
            self.run_git(repo, "config", "gensokyo.coAuthor", "true")
            (repo / "parser.txt").write_text("decoded timestamp\n", encoding="utf-8")
            self.run_git(repo, "add", "parser.txt")
            message_path = repo / "message.txt"
            original = (
                "Repair compatibility boundary\n\nKeep this body.\n\n"
                "Co-authored-by: Human <human@example.com>\n"
            )
            message_path.write_text(original, encoding="utf-8")
            for _ in range(2):
                self.run_helper(
                    repo,
                    "--message-file",
                    str(message_path),
                    "nitori-reverse-engineering",
                    "yukari-boundary-analysis",
                )
            updated = message_path.read_text(encoding="utf-8")
            self.assertTrue(updated.startswith(original))
            self.run_helper(
                repo,
                "--no-co-author",
                "--message-file",
                str(message_path),
                "nitori-reverse-engineering",
                "yukari-boundary-analysis",
            )
            self.assertEqual(message_path.read_text(encoding="utf-8"), updated)
            self.run_git(repo, "commit", "--quiet", "-F", str(message_path))
            committed = self.run_git(repo, "log", "-1", "--format=%B").stdout
            self.assertEqual(committed.count("Assisted-by: Nitori"), 1)
            self.assertEqual(committed.count("Assisted-by: Yukari"), 1)
            self.assertEqual(committed.count(PROJECT_CREDIT), 1)
            self.assertIn("Co-authored-by: Human <human@example.com>", committed)
            self.assertEqual(committed.strip(), updated.strip())


if __name__ == "__main__":
    unittest.main()
