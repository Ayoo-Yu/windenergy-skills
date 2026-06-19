#!/usr/bin/env python3
"""Collect windenergy-orchestrator outputs into a final manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


EXPECTED_OUTPUTS = [
    "project_state.json",
    "decision_log.md",
    "task_queue.md",
    "artifact_index.json",
    "automation_recipes.md",
    "workflow_profile.json",
    "final/paper.tex",
    "final/paper.pdf",
    "final/refs.bib",
    "literature/refs.bib",
    "outline/outline.json",
    "diagnostics/source_code_evidence_register.md",
    "diagnostics/claim_evidence_map.md",
    "diagnostics/mechanism_diagnostics.md",
    "diagnostics/profile_evidence_strength_audit.md",
    "diagnostics/profile_evidence_strength_audit.json",
    "diagnostics/mechanism_evidence_strength_audit.md",
    "diagnostics/mechanism_evidence_strength_audit.json",
    "drafts/paper_polished.tex",
    "audits/polishing_audit.md",
    "audits/writing_quality_audit.md",
    "audits/writing_quality_audit.json",
    "audits/writing_revision_plan.md",
    "audits/manuscript_quality_audit.md",
    "audits/manuscript_quality_audit.json",
    "audits/figure_consistency_audit.md",
    "audits/figure_consistency_audit.json",
    "audits/scientific_maturity_audit.md",
    "audits/scientific_maturity_audit.json",
    "audits/citation_audit.json",
    "audits/submission_audit.md",
]

CONTROL_FILES = {
    "project_state.json",
    "decision_log.md",
    "task_queue.md",
    "artifact_index.json",
    "automation_recipes.md",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def iter_values(value: Any):
    if isinstance(value, dict):
        for item in value.values():
            yield from iter_values(item)
    elif isinstance(value, list):
        for item in value:
            yield from iter_values(item)
    else:
        yield value


def citation_audit_ready(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    statuses = {str(value).upper() for value in iter_values(data)}
    return not (statuses & {"FAIL", "UNCHECKED", "NARRATIVE_WARNING", "SECTION_WARNING", "LANGUAGE_WARNING", "TONE_WARNING", "AUTHOR_INPUT_NEEDED"})


def json_audit_ready(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    status = str(data.get("status", "")).upper()
    if status:
        return status == "PASS"
    statuses = {str(value).upper() for value in iter_values(data)}
    return not (statuses & {"FAIL", "UNCHECKED", "NARRATIVE_WARNING", "SECTION_WARNING", "LANGUAGE_WARNING", "TONE_WARNING", "AUTHOR_INPUT_NEEDED"})


def submission_audit_ready(path: Path) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    return not any(token in text for token in ["FAIL", "UNCHECKED", "NARRATIVE_WARNING", "SECTION_WARNING", "LANGUAGE_WARNING", "TONE_WARNING"])


def polishing_audit_ready(path: Path) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    if re.search(r"AUTHOR_INPUT_NEEDED\s*:\s*(OPEN|UNRESOLVED|BLOCKED)", text, re.I):
        return False
    return not re.search(r"Claim risk\s*:\s*(OPEN|UNRESOLVED|BLOCKED)", text, re.I)


def scientific_maturity_ready(path: Path) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    match = re.search(r"Overall status\s*:\s*(PASS|FAIL|UNCHECKED|AUTHOR_INPUT_NEEDED|NARRATIVE_WARNING|SECTION_WARNING|LANGUAGE_WARNING|TONE_WARNING)", text, re.I)
    if match:
        return match.group(1).upper() == "PASS"
    if re.search(r"AUTHOR_INPUT_NEEDED\s*:\s*(OPEN|UNRESOLVED|BLOCKED)", text, re.I):
        return False
    return not any(token in text for token in ["FAIL", "UNCHECKED", "NARRATIVE_WARNING", "SECTION_WARNING", "LANGUAGE_WARNING", "TONE_WARNING"])


def writing_quality_ready(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    if str(data.get("status", "")).upper() != "PASS":
        return False
    statuses = {str(value).upper() for value in iter_values(data)}
    return not (statuses & {"FAIL", "UNCHECKED", "NARRATIVE_WARNING", "SECTION_WARNING", "LANGUAGE_WARNING", "TONE_WARNING", "AUTHOR_INPUT_NEEDED"})


def workbench_state_check(workspace: Path) -> tuple[bool, bool, str]:
    missing = [rel for rel in CONTROL_FILES if not (workspace / rel).exists()]
    if missing:
        return False, False, "missing workbench control files: " + ", ".join(sorted(missing))
    try:
        project = json.loads((workspace / "project_state.json").read_text(encoding="utf-8"))
        artifact_index = json.loads((workspace / "artifact_index.json").read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False, True, "workbench control JSON is invalid"
    if project.get("schema_version") != 1 or artifact_index.get("schema_version") != 1:
        return False, True, "workbench control schema_version must be 1"
    if project.get("project_status") not in {"active", "blocked", "ready"}:
        return False, True, "project_state.json project_status is invalid"
    if not isinstance(artifact_index.get("artifacts"), list):
        return False, True, "artifact_index.json artifacts must be a list"
    ready_claim = project.get("project_status") == "ready"
    return ready_claim, False, "workbench control files are valid"


def collect(workspace: Path) -> dict:
    files = []
    missing = []
    for rel in EXPECTED_OUTPUTS:
        path = workspace / rel
        if not path.exists():
            missing.append(rel)
            files.append({"path": rel, "exists": False})
            continue
        files.append(
            {
                "path": rel,
                "exists": True,
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )

    citation_ready = citation_audit_ready(workspace / "audits" / "citation_audit.json")
    submission_ready = submission_audit_ready(workspace / "audits" / "submission_audit.md")
    polishing_ready = polishing_audit_ready(workspace / "audits" / "polishing_audit.md")
    writing_ready = writing_quality_ready(workspace / "audits" / "writing_quality_audit.json")
    maturity_ready = scientific_maturity_ready(workspace / "audits" / "scientific_maturity_audit.md")
    manuscript_quality_ready = json_audit_ready(workspace / "audits" / "manuscript_quality_audit.json")
    figure_consistency_ready = json_audit_ready(workspace / "audits" / "figure_consistency_audit.json")
    profile_evidence_ready = json_audit_ready(workspace / "diagnostics" / "profile_evidence_strength_audit.json")
    mechanism_evidence_ready = profile_evidence_ready or json_audit_ready(workspace / "diagnostics" / "mechanism_evidence_strength_audit.json")
    final_ready = all((workspace / rel).exists() for rel in ["final/paper.tex", "final/paper.pdf"])
    workbench_ready, workbench_conflict, workbench_reason = workbench_state_check(workspace)
    core_ready = (
        citation_ready
        and submission_ready
        and polishing_ready
        and writing_ready
        and maturity_ready
        and manuscript_quality_ready
        and figure_consistency_ready
        and mechanism_evidence_ready
        and final_ready
    )

    if (
        core_ready
        and workbench_ready
    ):
        status = "PASS"
    elif workbench_conflict or (workbench_ready and not core_ready):
        status = "FAIL"
    elif missing:
        status = "UNCHECKED"
    else:
        status = "FAIL"

    return {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "workspace": str(workspace),
        "status": status,
        "ready": status == "PASS",
        "polishing_audit_ready": polishing_ready,
        "writing_quality_audit_ready": writing_ready,
        "manuscript_quality_ready": manuscript_quality_ready,
        "figure_consistency_ready": figure_consistency_ready,
        "mechanism_evidence_ready": mechanism_evidence_ready,
        "profile_evidence_ready": profile_evidence_ready,
        "scientific_maturity_audit_ready": maturity_ready,
        "citation_audit_ready": citation_ready,
        "submission_audit_ready": submission_ready,
        "final_files_ready": final_ready,
        "workbench_state_ready": workbench_ready,
        "workbench_state_reason": workbench_reason,
        "missing": missing,
        "files": files,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace")
    parser.add_argument(
        "--output",
        help="Manifest path. Defaults to WORKSPACE/final/final_manifest.json",
    )
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    manifest = collect(workspace)
    output = Path(args.output).resolve() if args.output else workspace / "final" / "final_manifest.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
    output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
