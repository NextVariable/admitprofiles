"""Verify a copied skill remains runnable without repository development files."""

import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from test_skill_helpers import ROOT, fixture

SKILL = ROOT / "skills/admission-intelligence"


class SkillPackageTests(unittest.TestCase):
    def test_copied_package_runs_both_helpers_without_repository(self):
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            package = work / "installed/admission-intelligence"
            shutil.copytree(
                SKILL, package, ignore=shutil.ignore_patterns("__pycache__")
            )
            inputs = {
                "validate_cases": fixture(),
                "work_months": {
                    "cutoff": "2021-01",
                    "intervals": [{"start": "2020-01", "end": None}],
                },
            }
            for tool, data in inputs.items():
                with self.subTest(tool=tool):
                    path = work / f"{tool}.json"
                    content = json.dumps(data)
                    path.write_text(content, encoding="utf-8")
                    result = subprocess.run(
                        [
                            sys.executable,
                            "-I",
                            str(package / "scripts" / f"{tool}.py"),
                            str(path),
                        ],
                        cwd=work,
                        capture_output=True,
                        text=True,
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(path.read_text(encoding="utf-8"), content)
                    if tool == "work_months":
                        self.assertEqual(json.loads(result.stdout)["min_months"], 12)

    def test_skill_references_remain_inside_installable_package(self):
        for document in [
            SKILL / "SKILL.md",
            *sorted((SKILL / "references").glob("*.md")),
        ]:
            for link in re.findall(
                r"\]\(([^)]+)\)", document.read_text(encoding="utf-8")
            ):
                if "://" in link or link.startswith("#"):
                    continue
                with self.subTest(document=document.name, link=link):
                    target = (document.parent / link.split("#", 1)[0]).resolve()
                    self.assertTrue(target.is_relative_to(SKILL.resolve()))
                    self.assertTrue(target.exists(), str(target))

    def test_current_repository_entry_links_resolve(self):
        for name in (
            "README.md",
            "CONTRIBUTING.md",
            "docs/architecture.md",
            "research/README.md",
            "evals/README.md",
            "docs/history/README.md",
        ):
            document = ROOT / name
            for link in re.findall(
                r"\]\(([^)]+)\)", document.read_text(encoding="utf-8")
            ):
                if "://" in link or link.startswith("#"):
                    continue
                with self.subTest(document=name, link=link):
                    target = (document.parent / link.split("#", 1)[0]).resolve()
                    self.assertTrue(target.is_relative_to(ROOT.resolve()))
                    self.assertTrue(target.exists(), str(target))
