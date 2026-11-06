"""Specs for the learning-loop CLIs: record-learning and sweep-learnings.

Each test stages copies of the two skills in a temp dir, points
their configs at a fake skill tree and log dir, and drives the
real CLIs, so the tools are specified by how they behave.
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

REPO_ROOT = Path(__file__).resolve().parent.parent
RECORD_SKILL = REPO_ROOT / "studio" / "learning" / "record-learning"
SWEEP_SKILL = REPO_ROOT / "studio" / "learning" / "sweep-learnings"


def stage(skill_source, dest, tree, log_dir):
    shutil.copytree(skill_source, dest,
                    ignore=shutil.ignore_patterns("__pycache__"))
    config = dest / "config.md"
    text = config.read_text()
    block = json.loads(re.search(r"```json\s*(.*?)```", text, re.S).group(1))
    block["skills_dirs"] = [str(tree)]
    block["log_dir"] = str(log_dir)
    config.write_text(re.sub(
        r"```json\s*.*?```",
        "```json\n" + json.dumps(block, indent=2) + "\n```",
        text, flags=re.S))
    return dest / "bin"


class LearningScriptsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.tree = root / "tree"
        (self.tree / "fake-skill").mkdir(parents=True)
        self.log_dir = root / "log"
        self.log = self.log_dir / "learnings.md"
        self.record = stage(RECORD_SKILL, root / "record-learning",
                            self.tree, self.log_dir) / "record-learning"
        self.sweep = stage(SWEEP_SKILL, root / "sweep-learnings",
                           self.tree, self.log_dir) / "sweep-learnings"
        self.today = datetime.now(
            ZoneInfo("America/Los_Angeles")).strftime("%Y-%m-%d")

    def tearDown(self):
        self.tmp.cleanup()

    def run_record(self, *args):
        return subprocess.run([sys.executable, str(self.record), *args],
                              capture_output=True, text=True)

    def run_sweep(self, *args):
        return subprocess.run([sys.executable, str(self.sweep), *args],
                              capture_output=True, text=True)


class RecordLearningTest(LearningScriptsTest):
    def test_records_a_learning_as_a_tagged_line_in_the_central_log(self):
        result = self.run_record("fake-skill", "Always test first.")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(
            f"- [{self.today}] [fake-skill] Always test first.",
            self.log.read_text())

    def test_tags_a_spanning_learning_cross_skill(self):
        result = self.run_record("cross-skill", "Applies everywhere.")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(f"- [{self.today}] [cross-skill] Applies everywhere.",
                      self.log.read_text())

    def test_rejects_a_skill_name_that_does_not_exist(self):
        result = self.run_record("no-such-skill", "Orphan learning.")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.log.exists())

    def test_resolves_a_legacy_prefixed_name_to_the_bare_tag(self):
        result = self.run_record("local-fake-skill", "Prefixed name.")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(f"- [{self.today}] [fake-skill] Prefixed name.",
                      self.log.read_text())


class SweepLearningsTest(LearningScriptsTest):
    def test_lists_every_pending_entry(self):
        self.run_record("fake-skill", "One.")
        self.run_record("cross-skill", "Two.")
        result = self.run_sweep()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("[fake-skill] One.", result.stdout)
        self.assertIn("[cross-skill] Two.", result.stdout)

    def test_reports_no_pending_learnings_when_the_log_is_empty(self):
        result = self.run_sweep()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("no pending learnings", result.stdout)

    def test_drop_removes_only_the_named_skills_entries(self):
        self.run_record("fake-skill", "Implemented.")
        self.run_record("cross-skill", "Still pending.")
        result = self.run_sweep("--drop", "fake-skill")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("[fake-skill] Implemented.", result.stdout)
        remaining = self.log.read_text()
        self.assertNotIn("Implemented.", remaining)
        self.assertIn("[cross-skill] Still pending.", remaining)

    def test_drop_for_a_skill_with_no_entries_changes_nothing(self):
        self.run_record("fake-skill", "Still pending.")
        before = self.log.read_text()
        result = self.run_sweep("--drop", "cross-skill")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("no pending learnings for cross-skill", result.stdout)
        self.assertEqual(self.log.read_text(), before)


if __name__ == "__main__":
    unittest.main()
