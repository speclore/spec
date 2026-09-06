#!/usr/bin/env python3
"""Validate the specification package, fixture expectations and example, read-only."""

import copy
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

from jsonschema import Draft202012Validator
from validate import MD, REPO, PROFILE, read_snapshot, schema_errors, validate


class ReleaseChecks(unittest.TestCase):
    def test_fixture_matrix(self):
        matrix = json.loads((REPO / "conformance/fixtures/cases.json").read_text())
        self.assertEqual(matrix["profile"], PROFILE)
        files, dirs, links = read_snapshot(REPO / matrix["base"])
        self.assertFalse(links)
        seen = set()
        for case in matrix["cases"]:
            with self.subTest(case=case["id"]):
                self.assertNotIn(case["id"], seen)
                seen.add(case["id"])
                candidate = copy.deepcopy(files)
                candidate_dirs = set(dirs)
                for change in case["changes"]:
                    path = change["path"]
                    if change.get("delete"):
                        del candidate[path]
                    elif "content" in change:
                        candidate[path] = change["content"].encode("utf-8")
                    else:
                        original = candidate[path].decode("utf-8")
                        self.assertIn(change["old"], original, "fixture mutation must match")
                        candidate[path] = original.replace(change["old"], change["value"], 1).encode("utf-8")
                if "extraFolders" in case:
                    extra = case["extraFolders"]
                    candidate_dirs.update(f"{extra['parent']}/extra-{i}" for i in range(extra["count"]))
                before = dict(candidate)
                report = validate(candidate, candidate_dirs)
                self.assertEqual(candidate, before, "validation must not mutate its input")
                self.assertFalse(schema_errors("diagnostic", report))
                self.assertEqual(report["valid"], case["valid"], report["diagnostics"])
                if not case["valid"]:
                    self.assertIn(case["code"], {d["code"] for d in report["diagnostics"]})
        print(f"\nVerified {len(seen)} snapshot cases ({sum(c['valid'] for c in matrix['cases'])} valid).")

    def test_all_schemas_are_well_formed(self):
        ids = set()
        for path in (REPO / "schemas").rglob("*.schema.json"):
            schema = json.loads(path.read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)
            self.assertNotIn(schema["$id"], ids)
            ids.add(schema["$id"])

    def test_report_validity_matches_errors(self):
        error = {"code": "C02", "severity": "error", "path": "x.md", "message": "invalid"}
        self.assertTrue(schema_errors("diagnostic", {"profile": PROFILE, "valid": True, "diagnostics": [error]}))
        self.assertTrue(schema_errors("diagnostic", {"profile": PROFILE, "valid": False, "diagnostics": []}))
        error["severity"] = "warning"
        self.assertFalse(schema_errors("diagnostic", {"profile": PROFILE, "valid": True, "diagnostics": [error]}))

    def test_reference_paths_and_exact_identifiers(self):
        guid = "11111111-1111-4111-8111-111111111111"
        for path in ("", "work", "work/one.md"):
            self.assertFalse(schema_errors("refs", {"guid": guid, "path": path, "refs": {}}))
        for path in ("/absolute", "../outside", "a/../b", "a//b", "a/", "a\\b", "a\nb", ".hidden"):
            self.assertTrue(schema_errors("refs", {"guid": guid, "path": path, "refs": {}}), path)
        self.assertTrue(schema_errors("refs", {"guid": guid + "\n", "path": "", "refs": {}}))

    def test_operation_acceptance_scenarios(self):
        fixture = json.loads((REPO / "conformance/fixtures/operations.json").read_text())
        self.assertEqual(fixture["profile"], PROFILE)
        self.assertEqual({s["id"] for s in fixture["scenarios"]}, {f"OP{i:02}" for i in range(1, 10)})
        for scenario in fixture["scenarios"]:
            for field in ("capability", "initial", "actions", "expected"):
                self.assertTrue(scenario[field])

    def test_example_cli_is_read_only(self):
        root = REPO / "examples/core-project"
        before = read_snapshot(root)
        result = subprocess.run([sys.executable, str(REPO / "conformance/validate.py"), str(root)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertTrue(json.loads(result.stdout)["valid"])
        self.assertEqual(before, read_snapshot(root))

    def test_symlinks_are_not_followed(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "escape").symlink_to(REPO / "examples/core-project", target_is_directory=True)
            files, dirs, links = read_snapshot(root)
            self.assertEqual(files, {})
            self.assertEqual(links, ["escape"])
            result = subprocess.run([sys.executable, str(REPO / "conformance/validate.py"), str(root)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertIn("C05", {d["code"] for d in json.loads(result.stdout)["diagnostics"]})

    def test_cli_missing_path(self):
        with tempfile.TemporaryDirectory() as temporary:
            missing = Path(temporary) / "not-created"
            result = subprocess.run([sys.executable, str(REPO / "conformance/validate.py"), str(missing)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)

    def test_editorial_links_and_core_placeholders(self):
        paths = [REPO / p for p in ("README.md", "governance.md", "changelog.md")]
        for directory in ("specification", "schemas", "conformance", "examples", "backlog"):
            paths.extend((REPO / directory).rglob("*.md"))
        for path in paths:
            if "core-project" in path.parts:
                continue
            text = path.read_text(encoding="utf-8")
            targets = [child.attrGet("href") for token in MD.parse(text)
                       for child in (token.children or []) if child.type == "link_open"]
            for target in targets:
                target = target.split("#", 1)[0]
                if not target or ":" in target or "<" in target:
                    continue
                self.assertTrue((path.parent / target).exists(), f"{path}: broken link {target}")
        core = (REPO / "specification/core/core.md").read_text()
        self.assertFalse(re.search(r"(?i)to be (defined|fixed)|TBD|TODO", core))
        criteria = (REPO / "conformance/README.md").read_text()
        for i in range(1, 11):
            self.assertIn(f"C{i:02}", core)
            self.assertIn(f"C{i:02}", criteria)


if __name__ == "__main__":
    unittest.main(verbosity=2)
