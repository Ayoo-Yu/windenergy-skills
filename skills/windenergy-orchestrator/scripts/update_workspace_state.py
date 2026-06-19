#!/usr/bin/env python3
"""Refresh windenergy-orchestrator workbench state files."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from collect_outputs import EXPECTED_OUTPUTS, collect  # noqa: E402
from init_workspace import CONTROL_FILES, init_control_files, utc_now  # noqa: E402
from validate_stage_outputs import STAGES, validate_stages  # noqa: E402
from validate_workspace import validate_workspace  # noqa: E402


BLOCKING_STATUSES = {"FAIL", "AUTHOR_INPUT_NEEDED"}
CONTROL_STAGE = "workbench_state"
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".svg"}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_task_queue(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    tasks: list[dict[str, str]] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) < 5:
            continue
        if cells[0].lower() == "id" or set(cells[0]) <= {"-"}:
            continue
        tasks.append(
            {
                "id": cells[0],
                "status": cells[1],
                "trigger": cells[2],
                "task": cells[3],
                "completion": cells[4],
            }
        )
    return tasks


def summarize_decisions(path: Path) -> list[str]:
    if not path.exists():
        return []
    summary: list[str] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped == "No durable decisions recorded yet.":
            continue
        summary.append(stripped)
        if len(summary) == 10:
            break
    return summary


def artifact_type(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".json":
        return "json"
    if suffix == ".md":
        return "markdown"
    if suffix == ".tex":
        return "latex"
    if suffix == ".bib":
        return "bibtex"
    if suffix == ".pdf":
        return "pdf"
    if suffix in IMAGE_SUFFIXES:
        return "figure"
    return "file"


def artifact_stage(rel: str) -> str:
    if rel in CONTROL_FILES:
        return CONTROL_STAGE
    if rel == "workflow_profile.json":
        return "profile"
    if rel.startswith("inputs/"):
        return "input"
    if rel.startswith("outline/"):
        return "outline"
    if rel.startswith("diagnostics/"):
        return "diagnostics"
    if rel.startswith("literature/"):
        return "literature"
    if rel.startswith("figures/"):
        return "figures"
    if rel.startswith("drafts/"):
        return "draft"
    if rel.startswith("refinement/"):
        return "refinement"
    if rel.startswith("audits/"):
        return "audit"
    if rel.startswith("final/"):
        return "final_package"
    return "workspace"


def build_artifact_index(workspace: Path, rels: list[str]) -> dict:
    artifacts = []
    seen: set[str] = set()
    for rel in rels:
        if rel in seen:
            continue
        seen.add(rel)
        path = workspace / rel
        if not path.exists() or not path.is_file():
            continue
        stat = path.stat()
        artifacts.append(
            {
                "path": rel,
                "type": artifact_type(path),
                "stage": artifact_stage(rel),
                "bytes": stat.st_size,
                "sha256": sha256_file(path),
                "generated_at": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
                "review_status": "unchecked",
            }
        )
    return {
        "schema_version": 1,
        "updated_at": utc_now(),
        "artifacts": artifacts,
    }


def first_relevant_stage(stage_report: dict[str, Any]) -> dict[str, Any]:
    stages = [
        stage
        for stage in stage_report.get("stages", [])
        if stage.get("stage") not in {CONTROL_STAGE, "workbench_state_consistency", "final_manifest_consistency"}
    ]
    for status in ["FAIL", "UNCHECKED"]:
        for stage in stages:
            if stage.get("status") == status:
                return stage
    for stage in reversed(stages):
        if stage.get("status") == "PASS":
            return stage
    return {"stage": "input", "status": "UNCHECKED", "missing": [], "reason": "no stage report available"}


def core_manifest_ready(manifest: dict[str, Any]) -> bool:
    keys = [
        "polishing_audit_ready",
        "manuscript_quality_ready",
        "figure_consistency_ready",
        "mechanism_evidence_ready",
        "scientific_maturity_audit_ready",
        "citation_audit_ready",
        "submission_audit_ready",
        "final_files_ready",
    ]
    return all(bool(manifest.get(key)) for key in keys)


def next_action_for(stage: dict[str, Any], ready: bool) -> str:
    if ready:
        return "Review final/final_manifest.json and submit the ready package."
    name = str(stage.get("stage", "input"))
    status = str(stage.get("status", "UNCHECKED"))
    missing = stage.get("missing") or []
    reason = str(stage.get("reason", "")).strip()
    if status == "FAIL":
        detail = reason or "stage validation failed"
        return f"Resolve the blocking issue in {name}: {detail}."
    if missing:
        return f"Generate or provide missing artifacts for {name}: {', '.join(map(str, missing))}."
    return f"Continue the windenergy-orchestrator workflow at {name}."


def blocking_items_from(stage_report: dict[str, Any]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for stage in stage_report.get("stages", []):
        name = stage.get("stage")
        status = str(stage.get("status", "")).upper()
        if name in {CONTROL_STAGE, "workbench_state_consistency", "final_manifest_consistency"}:
            continue
        reason = stage.get("reason") or ""
        missing = stage.get("missing") or []
        if status in BLOCKING_STATUSES:
            items.append(
                {
                    "stage": name,
                    "status": status,
                    "source": reason or "stage validator",
                    "requires_author": "AUTHOR_INPUT_NEEDED" in reason,
                }
            )
        elif status == "UNCHECKED" and name in {"profile", "input"}:
            items.append(
                {
                    "stage": name,
                    "status": status,
                    "source": "missing required workspace input: " + ", ".join(map(str, missing)),
                    "requires_author": True,
                }
            )
    return items


def update_state(workspace: Path) -> dict:
    workspace = workspace.resolve()
    init_control_files(workspace, overwrite=False)

    workspace_report = validate_workspace(workspace)
    stage_report = validate_stages(workspace)
    manifest = collect(workspace)
    current = first_relevant_stage(stage_report)
    ready = stage_report.get("status") == "PASS" and core_manifest_ready(manifest)
    blocking_items = blocking_items_from(stage_report)

    if ready:
        project_status = "ready"
    elif blocking_items:
        project_status = "blocked"
    else:
        project_status = "active"

    project_state = {
        "schema_version": 1,
        "project_status": project_status,
        "current_stage": current.get("stage", "input"),
        "stage_status": "PASS" if ready else current.get("status", "UNCHECKED"),
        "next_action": next_action_for(current, ready),
        "blocking_items": blocking_items,
        "queued_tasks": parse_task_queue(workspace / "task_queue.md"),
        "author_decisions_summary": summarize_decisions(workspace / "decision_log.md"),
        "workspace": str(workspace),
        "workspace_validator_status": workspace_report.get("status", "UNCHECKED"),
        "stage_validator_status": stage_report.get("status", "UNCHECKED"),
        "manifest_status": manifest.get("status", "UNCHECKED"),
        "updated_at": utc_now(),
    }

    artifact_rels = list(EXPECTED_OUTPUTS) + CONTROL_FILES + ["final/final_manifest.json"]
    artifact_index = build_artifact_index(workspace, artifact_rels)
    (workspace / "project_state.json").write_text(
        json.dumps(project_state, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (workspace / "artifact_index.json").write_text(
        json.dumps(artifact_index, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    final_stage_report = validate_stages(workspace)
    return {
        "workspace": str(workspace),
        "status": project_state["project_status"],
        "current_stage": project_state["current_stage"],
        "stage_status": project_state["stage_status"],
        "next_action": project_state["next_action"],
        "blocking_items": project_state["blocking_items"],
        "artifact_count": len(artifact_index["artifacts"]),
        "workspace_report_status": workspace_report.get("status", "UNCHECKED"),
        "stage_report_status": final_stage_report.get("status", "UNCHECKED"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace")
    parser.add_argument("--json-output", help="Optional path to write JSON report")
    args = parser.parse_args()

    report = update_state(Path(args.workspace))
    text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.json_output:
        Path(args.json_output).write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if report["stage_report_status"] != "FAIL" else 1


if __name__ == "__main__":
    raise SystemExit(main())
