#!/usr/bin/env python3
"""Validate windenergy-orchestrator stage outputs."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


STAGES = {
    "workbench_state": [
        "project_state.json",
        "decision_log.md",
        "task_queue.md",
        "artifact_index.json",
        "automation_recipes.md",
    ],
    "profile": ["workflow_profile.json"],
    "input": ["inputs/idea.md", "inputs/experimental_log.md", "inputs/template.tex", "inputs/conference_guidelines.md"],
    "outline": ["outline/outline.json"],
    "source_evidence": ["diagnostics/source_code_evidence_register.md"],
    "claim_evidence": ["diagnostics/claim_evidence_map.md"],
    "mechanism_diagnostics": ["diagnostics/mechanism_diagnostics.md"],
    "literature": ["literature/refs.bib", "literature/search_log.md"],
    "figures": ["figures/captions.json", "figures/figure_text_audit.md"],
    "draft": ["drafts/paper.tex"],
    "polishing": ["drafts/paper_polished.tex", "audits/polishing_audit.md"],
    "writing_quality": [
        "audits/writing_quality_audit.json",
        "audits/writing_quality_audit.md",
        "audits/writing_revision_plan.md",
    ],
    "manuscript_quality": ["audits/manuscript_quality_audit.json", "audits/manuscript_quality_audit.md"],
    "figure_consistency": ["audits/figure_consistency_audit.json", "audits/figure_consistency_audit.md"],
    "mechanism_evidence_strength": [
        "diagnostics/profile_evidence_strength_audit.json",
        "diagnostics/profile_evidence_strength_audit.md",
    ],
    "legacy_mechanism_evidence_strength": [
        "diagnostics/mechanism_evidence_strength_audit.json",
        "diagnostics/mechanism_evidence_strength_audit.md",
    ],
    "scientific_maturity": ["audits/scientific_maturity_audit.md"],
    "citation_audit": ["audits/citation_audit.json"],
    "submission_audit": ["audits/submission_audit.md"],
    "final_package": ["final/paper.tex", "final/paper.pdf"],
}

PROJECT_STATUSES = {"active", "blocked", "ready"}
STAGE_STATUSES = {
    "PASS",
    "FAIL",
    "UNCHECKED",
    "AUTHOR_INPUT_NEEDED",
    "NARRATIVE_WARNING",
    "SECTION_WARNING",
    "LANGUAGE_WARNING",
    "TONE_WARNING",
}


def iter_values(value: Any):
    if isinstance(value, dict):
        for item in value.values():
            yield from iter_values(item)
    elif isinstance(value, list):
        for item in value:
            yield from iter_values(item)
    else:
        yield value


def contains_bad_audit_status(path: Path) -> bool:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return True
    statuses = {str(value).upper() for value in iter_values(data)}
    return bool(statuses & {"FAIL", "UNCHECKED", "NARRATIVE_WARNING", "SECTION_WARNING", "LANGUAGE_WARNING", "TONE_WARNING", "AUTHOR_INPUT_NEEDED"})


def contains_unresolved_polishing_issue(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="replace")
    if re.search(r"AUTHOR_INPUT_NEEDED\s*:\s*(OPEN|UNRESOLVED|BLOCKED)", text, re.I):
        return True
    return bool(re.search(r"Claim risk\s*:\s*(OPEN|UNRESOLVED|BLOCKED)", text, re.I))


def contains_blocking_markdown_issue(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="replace")
    match = re.search(r"Overall status\s*:\s*(PASS|FAIL|UNCHECKED|AUTHOR_INPUT_NEEDED|NARRATIVE_WARNING|SECTION_WARNING|LANGUAGE_WARNING|TONE_WARNING)", text, re.I)
    if match:
        return match.group(1).upper() != "PASS"
    if re.search(r"AUTHOR_INPUT_NEEDED\s*:\s*(OPEN|UNRESOLVED|BLOCKED)", text, re.I):
        return True
    return bool(re.search(r"\b(FAIL|UNCHECKED|NARRATIVE_WARNING|SECTION_WARNING|LANGUAGE_WARNING|TONE_WARNING)\b", text))


def manifest_claims_ready(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except json.JSONDecodeError:
        text = path.read_text(encoding="utf-8", errors="replace")
        return bool(re.search(r"\b(status\s*[:=]\s*ready|ready\s*[:=]\s*true)\b", text, re.I))
    status = str(data.get("status", "")).strip().lower()
    ready = data.get("ready")
    return status in {"ready", "pass"} or ready is True


def validate_workbench_state(workspace: Path) -> tuple[str, str]:
    project_path = workspace / "project_state.json"
    artifact_path = workspace / "artifact_index.json"
    decision_path = workspace / "decision_log.md"
    queue_path = workspace / "task_queue.md"
    recipes_path = workspace / "automation_recipes.md"

    try:
        project = json.loads(project_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return "FAIL", "project_state.json is invalid JSON"
    try:
        artifact_index = json.loads(artifact_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return "FAIL", "artifact_index.json is invalid JSON"

    if project.get("schema_version") != 1:
        return "FAIL", "project_state.json schema_version must be 1"
    if project.get("project_status") not in PROJECT_STATUSES:
        return "FAIL", "project_state.json project_status is invalid"
    known_stages = set(STAGES) - {"workbench_state"}
    if project.get("current_stage") not in known_stages:
        return "FAIL", "project_state.json current_stage is not a known stage"
    if project.get("stage_status") not in STAGE_STATUSES:
        return "FAIL", "project_state.json stage_status is invalid"
    if not isinstance(project.get("next_action"), str) or not project.get("next_action").strip():
        return "FAIL", "project_state.json next_action is missing"
    for key in ["blocking_items", "queued_tasks", "author_decisions_summary"]:
        if not isinstance(project.get(key), list):
            return "FAIL", f"project_state.json {key} must be a list"
    if not isinstance(project.get("updated_at"), str) or not project.get("updated_at").strip():
        return "FAIL", "project_state.json updated_at is missing"

    if artifact_index.get("schema_version") != 1:
        return "FAIL", "artifact_index.json schema_version must be 1"
    if not isinstance(artifact_index.get("artifacts"), list):
        return "FAIL", "artifact_index.json artifacts must be a list"
    if not decision_path.read_text(encoding="utf-8", errors="replace").strip():
        return "FAIL", "decision_log.md is empty"
    if "| id | status | trigger | task | completion |" not in queue_path.read_text(
        encoding="utf-8",
        errors="replace",
    ):
        return "FAIL", "task_queue.md is missing the queue table"
    recipes = recipes_path.read_text(encoding="utf-8", errors="replace")
    for heading in ["Compile Check", "Literature Update Check", "Reviewer Feedback Check", "Blocking Item Summary"]:
        if heading not in recipes:
            return "FAIL", f"automation_recipes.md missing {heading}"
    return "PASS", "workbench control files are valid"


def validate_stages(workspace: Path) -> dict:
    stages = []
    for name, rels in STAGES.items():
        missing = [rel for rel in rels if not (workspace / rel).exists()]
        if missing:
            stages.append({"stage": name, "status": "UNCHECKED", "missing": missing})
            continue

        status = "PASS"
        reason = "required artifacts exist"
        if name == "workbench_state":
            status, reason = validate_workbench_state(workspace)
        if name == "citation_audit" and contains_bad_audit_status(workspace / "audits" / "citation_audit.json"):
            status = "FAIL"
            reason = "citation audit contains FAIL, UNCHECKED, or invalid JSON"
        if name == "manuscript_quality" and contains_bad_audit_status(workspace / "audits" / "manuscript_quality_audit.json"):
            status = "FAIL"
            reason = "manuscript quality audit contains FAIL, UNCHECKED, or invalid JSON"
        if name == "figure_consistency" and contains_bad_audit_status(workspace / "audits" / "figure_consistency_audit.json"):
            status = "FAIL"
            reason = "figure consistency audit contains FAIL, UNCHECKED, or invalid JSON"
        if name == "mechanism_evidence_strength" and contains_bad_audit_status(workspace / "diagnostics" / "profile_evidence_strength_audit.json"):
            status = "FAIL"
            reason = "profile evidence strength audit contains blocking status or invalid JSON"
        if name == "legacy_mechanism_evidence_strength" and contains_bad_audit_status(workspace / "diagnostics" / "mechanism_evidence_strength_audit.json"):
            status = "FAIL"
            reason = "legacy mechanism evidence strength audit contains blocking status or invalid JSON"
        if name == "submission_audit":
            text = (workspace / "audits" / "submission_audit.md").read_text(encoding="utf-8", errors="replace")
            if any(token in text for token in ["FAIL", "UNCHECKED", "NARRATIVE_WARNING", "SECTION_WARNING", "LANGUAGE_WARNING", "TONE_WARNING"]):
                status = "FAIL"
                reason = "submission audit contains blocking status"
        if name == "polishing":
            if contains_unresolved_polishing_issue(workspace / "audits" / "polishing_audit.md"):
                status = "FAIL"
                reason = "polishing audit contains unresolved Claim risk or AUTHOR_INPUT_NEEDED"
        if name == "writing_quality" and contains_bad_audit_status(workspace / "audits" / "writing_quality_audit.json"):
            status = "FAIL"
            reason = "writing quality audit contains blocking narrative, section, language, tone, FAIL, UNCHECKED, or invalid JSON"
        if name == "scientific_maturity":
            if contains_blocking_markdown_issue(workspace / "audits" / "scientific_maturity_audit.md"):
                status = "FAIL"
                reason = "scientific maturity audit contains a blocking issue"
        stages.append({"stage": name, "status": status, "missing": [], "reason": reason})

    statuses = {stage["status"] for stage in stages}
    if "FAIL" in statuses:
        overall = "FAIL"
    elif "UNCHECKED" in statuses:
        overall = "UNCHECKED"
    else:
        overall = "PASS"

    project_state = workspace / "project_state.json"
    if project_state.exists():
        try:
            project = json.loads(project_state.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            project = {}
        other_statuses = {
            stage["status"]
            for stage in stages
            if stage["stage"] not in {"workbench_state"}
        }
        if project.get("project_status") == "ready" and other_statuses != {"PASS"}:
            stages.append(
                {
                    "stage": "workbench_state_consistency",
                    "status": "FAIL",
                    "missing": [],
                    "reason": "project_state.json claims ready while required stages are not PASS",
                }
            )
            overall = "FAIL"

    ready_manifests = [
        str(path.relative_to(workspace))
        for path in [workspace / "final" / "final_manifest.json", workspace / "final_manifest.json"]
        if manifest_claims_ready(path)
    ]
    if ready_manifests and overall != "PASS":
        stages.append(
            {
                "stage": "final_manifest_consistency",
                "status": "FAIL",
                "missing": [],
                "reason": "manifest claims ready while required windenergy-orchestrator stages are not PASS: "
                + ", ".join(ready_manifests),
            }
        )
        overall = "FAIL"
    return {"workspace": str(workspace), "status": overall, "stages": stages}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace")
    parser.add_argument("--json-output", help="Optional path to write JSON report")
    parser.add_argument("--strict", action="store_true", help="Return nonzero for UNCHECKED")
    args = parser.parse_args()

    report = validate_stages(Path(args.workspace).resolve())
    text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.json_output:
        Path(args.json_output).write_text(text, encoding="utf-8")
    print(text, end="")
    if report["status"] == "FAIL" or (args.strict and report["status"] == "UNCHECKED"):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
