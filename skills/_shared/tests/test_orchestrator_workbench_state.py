from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = ROOT / "windenergy-orchestrator" / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from init_workspace import CONTROL_FILES, init_workspace  # noqa: E402
from update_workspace_state import update_state  # noqa: E402
from validate_stage_outputs import validate_stages  # noqa: E402


class OrchestratorWorkbenchStateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="renewable_workbench_test_"))
        self.source = self.tmp / "source"
        self.workspace = self.tmp / "workspace"
        self.source.mkdir()

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp)

    def test_init_workspace_creates_control_files(self) -> None:
        init_workspace(self.source, self.workspace, overwrite=False)

        for rel in CONTROL_FILES:
            self.assertTrue((self.workspace / rel).exists(), rel)
        state = json.loads((self.workspace / "project_state.json").read_text(encoding="utf-8"))
        self.assertEqual(state["schema_version"], 1)
        self.assertEqual(state["project_status"], "active")
        self.assertEqual(state["current_stage"], "input")

    def test_init_missing_preserves_existing_control_files(self) -> None:
        self.workspace.mkdir()
        sentinel = {"schema_version": 1, "sentinel": True}
        (self.workspace / "project_state.json").write_text(json.dumps(sentinel), encoding="utf-8")

        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_DIR / "init_workspace.py"),
                "--init-missing",
                "--workspace",
                str(self.workspace),
            ],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            json.loads((self.workspace / "project_state.json").read_text(encoding="utf-8")),
            sentinel,
        )
        for rel in CONTROL_FILES:
            self.assertTrue((self.workspace / rel).exists(), rel)

    def test_update_state_missing_inputs_targets_input(self) -> None:
        init_workspace(self.source, self.workspace, overwrite=False)

        report = update_state(self.workspace)
        state = json.loads((self.workspace / "project_state.json").read_text(encoding="utf-8"))

        self.assertEqual(report["current_stage"], "input")
        self.assertEqual(state["current_stage"], "input")
        self.assertEqual(state["stage_status"], "UNCHECKED")
        self.assertIn("inputs", state["next_action"])

    def test_update_state_failure_records_blocker(self) -> None:
        init_workspace(self.source, self.workspace, overwrite=False)
        (self.workspace / "audits").mkdir(exist_ok=True)
        (self.workspace / "audits" / "citation_audit.json").write_text(
            json.dumps({"status": "FAIL"}, indent=2),
            encoding="utf-8",
        )

        report = update_state(self.workspace)
        state = json.loads((self.workspace / "project_state.json").read_text(encoding="utf-8"))

        self.assertEqual(report["status"], "blocked")
        self.assertTrue(any(item["stage"] == "citation_audit" for item in state["blocking_items"]))

    def write_ready_workspace(self) -> None:
        init_workspace(self.source, self.workspace, overwrite=False)
        required_text = {
            "inputs/idea.md": "Idea",
            "inputs/experimental_log.md": "Experiment log",
            "inputs/template.tex": "\\documentclass{article}\n\\begin{document}\n\\end{document}\n",
            "inputs/conference_guidelines.md": "Applied Energy",
            "diagnostics/source_code_evidence_register.md": "PASS",
            "diagnostics/claim_evidence_map.md": "PASS",
            "diagnostics/mechanism_diagnostics.md": "PASS",
            "diagnostics/profile_evidence_strength_audit.md": "Overall status: PASS",
            "diagnostics/mechanism_evidence_strength_audit.md": "Overall status: PASS",
            "literature/refs.bib": "@article{a, title={A}}\n",
            "literature/search_log.md": "PASS",
            "figures/figure_text_audit.md": "PASS",
            "drafts/paper.tex": "\\documentclass{article}\n",
            "drafts/paper_polished.tex": "\\documentclass{article}\n",
            "audits/polishing_audit.md": "Overall status: PASS",
            "audits/writing_quality_audit.md": "Overall status: PASS",
            "audits/writing_revision_plan.md": "No blocking writing revisions are required.",
            "audits/manuscript_quality_audit.md": "Overall status: PASS",
            "audits/figure_consistency_audit.md": "Overall status: PASS",
            "audits/scientific_maturity_audit.md": "Overall status: PASS",
            "audits/submission_audit.md": "Overall status: PASS",
            "final/paper.tex": "\\documentclass{article}\n",
            "final/refs.bib": "@article{a, title={A}}\n",
        }
        required_json = {
            "outline/outline.json": {"status": "PASS"},
            "figures/captions.json": {"status": "PASS"},
            "diagnostics/profile_evidence_strength_audit.json": {"status": "PASS"},
            "diagnostics/mechanism_evidence_strength_audit.json": {"status": "PASS"},
            "audits/manuscript_quality_audit.json": {"status": "PASS"},
            "audits/figure_consistency_audit.json": {"status": "PASS"},
            "audits/scientific_maturity_audit.json": {"status": "PASS"},
            "audits/citation_audit.json": {"status": "PASS"},
            "audits/writing_quality_audit.json": {
                "status": "PASS",
                "items": [{"check": "central_argument_alignment", "status": "PASS"}],
            },
        }
        for rel, content in required_text.items():
            path = self.workspace / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        for rel, content in required_json.items():
            path = self.workspace / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(content, indent=2), encoding="utf-8")
        (self.workspace / "final" / "paper.pdf").write_bytes(b"%PDF-1.4\n")

    def test_update_state_ready_and_artifact_index_hash(self) -> None:
        self.write_ready_workspace()

        report = update_state(self.workspace)
        state = json.loads((self.workspace / "project_state.json").read_text(encoding="utf-8"))
        artifact_index = json.loads((self.workspace / "artifact_index.json").read_text(encoding="utf-8"))

        self.assertEqual(report["status"], "ready")
        self.assertEqual(state["project_status"], "ready")
        self.assertEqual(report["stage_report_status"], "PASS")
        artifacts = {item["path"]: item for item in artifact_index["artifacts"]}
        self.assertIn("final/paper.pdf", artifacts)
        self.assertEqual(len(artifacts["final/paper.pdf"]["sha256"]), 64)

    def test_ready_project_state_conflict_fails_validator(self) -> None:
        init_workspace(self.source, self.workspace, overwrite=False)
        state = {
            "schema_version": 1,
            "project_status": "ready",
            "current_stage": "final_package",
            "stage_status": "PASS",
            "next_action": "Review final/final_manifest.json and submit the ready package.",
            "blocking_items": [],
            "queued_tasks": [],
            "author_decisions_summary": [],
            "updated_at": "2026-06-04T00:00:00+00:00",
        }
        (self.workspace / "project_state.json").write_text(json.dumps(state, indent=2), encoding="utf-8")

        report = validate_stages(self.workspace)

        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any(stage["stage"] == "workbench_state_consistency" for stage in report["stages"]))

    def test_legacy_workspace_missing_controls_is_unchecked(self) -> None:
        self.workspace.mkdir()

        report = validate_stages(self.workspace)

        self.assertEqual(report["status"], "UNCHECKED")
        self.assertTrue(any(stage["stage"] == "workbench_state" for stage in report["stages"]))


if __name__ == "__main__":
    unittest.main()
