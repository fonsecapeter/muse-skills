"""Specs for bin/link-skills and bin/verify.

Each test builds a scratch repo and destination in a temp dir and
drives the real CLIs, so the tools are specified by how they
behave, not by their internals.
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LINK_SKILLS = REPO_ROOT / "bin" / "link-skills"
VERIFY = REPO_ROOT / "bin" / "verify"

ROSTER = [
    {"name": "simi-claims", "bucket": "simi"},
    {"name": "learning-loop", "bucket": "studio"},
]


class CliTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.repo = root / "repo"
        self.dest = root / "dest"
        self.dest.mkdir(parents=True)
        for entry in ROSTER:
            skill = self.repo / entry["bucket"] / entry["name"]
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text(f"# {entry['name']}\n")
        (self.repo / "manifest.json").write_text(
            json.dumps({"name": "test", "skills": ROSTER})
        )

    def tearDown(self):
        self.tmp.cleanup()

    def run_link(self, *extra):
        return subprocess.run(
            [sys.executable, str(LINK_SKILLS), "--repo", str(self.repo),
             "--dest", str(self.dest), *extra],
            capture_output=True, text=True,
        )

    def run_verify(self):
        return subprocess.run(
            [sys.executable, str(VERIFY), "--repo", str(self.repo),
             "--dest", str(self.dest)],
            capture_output=True, text=True,
        )


class LinkSkillsTest(CliTestCase):
    def test_links_every_roster_skill_flat_into_the_destination(self):
        result = self.run_link()
        self.assertEqual(result.returncode, 0, result.stderr)
        for entry in ROSTER:
            target = self.dest / entry["name"]
            self.assertTrue(target.is_symlink())
            self.assertEqual(
                target.readlink(),
                self.repo / entry["bucket"] / entry["name"],
            )

    def test_a_second_run_creates_nothing(self):
        self.run_link()
        result = self.run_link()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("linked", result.stdout)
        self.assertIn("ok simi-claims", result.stdout)

    def test_check_passes_once_everything_is_linked(self):
        self.run_link()
        result = self.run_link("--check")
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_check_names_a_missing_link_as_drift(self):
        self.run_link()
        (self.dest / "simi-claims").unlink()
        result = self.run_link("--check")
        self.assertEqual(result.returncode, 1)
        self.assertIn("simi-claims", result.stdout)

    def test_refuses_to_replace_a_real_directory_and_leaves_it_untouched(self):
        real = self.dest / "simi-claims"
        real.mkdir()
        (real / "keep.txt").write_text("mine")
        result = self.run_link()
        self.assertEqual(result.returncode, 1)
        self.assertFalse(real.is_symlink())
        self.assertEqual((real / "keep.txt").read_text(), "mine")
        # Nothing else was linked either: the refusal happens first.
        self.assertFalse((self.dest / "learning-loop").exists())

    def test_ignores_repo_folders_the_manifest_does_not_list(self):
        draft = self.repo / "simi" / "draft-skill"
        draft.mkdir()
        (draft / "SKILL.md").write_text("# draft\n")
        result = self.run_link()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.dest / "draft-skill").exists())

    def test_relinks_a_symlink_pointing_at_the_wrong_source(self):
        elsewhere = self.repo / "elsewhere"
        elsewhere.mkdir()
        (self.dest / "simi-claims").symlink_to(elsewhere)
        result = self.run_link()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            (self.dest / "simi-claims").readlink(),
            self.repo / "simi" / "simi-claims",
        )


class VerifyTest(CliTestCase):
    def test_passes_when_the_roster_and_links_agree(self):
        self.run_link()
        result = self.run_verify()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_fails_when_a_roster_skill_has_no_skill_md(self):
        (self.repo / "simi" / "simi-claims" / "SKILL.md").unlink()
        self.run_link()
        result = self.run_verify()
        self.assertEqual(result.returncode, 1)
        self.assertIn("SKILL.md", result.stdout)

    def test_fails_when_a_link_is_missing(self):
        result = self.run_verify()
        self.assertEqual(result.returncode, 1)


if __name__ == "__main__":
    unittest.main()
