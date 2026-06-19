#!/usr/bin/env python3
"""Initialize a windenergy-orchestrator workspace from an experiment folder."""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


DIRS = [
    "inputs/figures",
    "inputs/source_materials",
    "diagnostics",
    "outline",
    "literature",
    "figures",
    "drafts",
    "refinement",
    "audits",
    "final",
]


SOURCE_MATERIALS = [
    "EXPERIMENT_REPORT_CLEAN_CN.md",
    "EXPERIMENT_RESULTS_REPORT.md",
    "EXPERIMENT_TRACEABILITY.md",
    "CURRENT_STATUS_AND_NEXT_PLAN.md",
    "PAPER_POSITIONING_MATERIAL_CN.md",
]

CONTROL_FILES = [
    "project_state.json",
    "decision_log.md",
    "task_queue.md",
    "artifact_index.json",
    "automation_recipes.md",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def default_project_state(workspace: Path) -> dict:
    now = utc_now()
    return {
        "schema_version": 1,
        "project_status": "active",
        "current_stage": "input",
        "stage_status": "UNCHECKED",
        "next_action": "Validate workspace inputs and complete any missing required files.",
        "blocking_items": [],
        "queued_tasks": [],
        "author_decisions_summary": [],
        "workspace": str(workspace),
        "workspace_validator_status": "UNCHECKED",
        "stage_validator_status": "UNCHECKED",
        "updated_at": now,
    }


def default_artifact_index() -> dict:
    return {
        "schema_version": 1,
        "updated_at": utc_now(),
        "artifacts": [],
    }


def default_decision_log() -> str:
    return (
        "# Decision Log\n\n"
        "Record durable author decisions, steering notes, reviewer judgments, "
        "scope choices, and constraints that future runs must preserve.\n\n"
        "## Active Decisions\n\n"
        "No durable decisions recorded yet.\n"
    )


def default_task_queue() -> str:
    return (
        "# Task Queue\n\n"
        "| id | status | trigger | task | completion |\n"
        "|---|---|---|---|---|\n"
    )


def default_automation_recipes() -> str:
    return (
        "# Automation Recipes\n\n"
        "Use these recipes for thread automations that return to this workspace. "
        "Every recipe starts by reading `project_state.json`, `task_queue.md`, "
        "and `decision_log.md`. Do not send external messages automatically. "
        "Draft replies or next actions for author review.\n\n"
        "## Compile Check\n\n"
        "1. Read `project_state.json` and confirm the current stage.\n"
        "2. If `final/paper.tex` or `drafts/paper_polished.tex` exists, run the "
        "configured compile check.\n"
        "3. Update `task_queue.md` with any compile failure and mark the task "
        "`AUTHOR_INPUT_NEEDED` only when an author fact or file is missing.\n"
        "4. Refresh `project_state.json` with `update_workspace_state.py`.\n\n"
        "## Literature Update Check\n\n"
        "1. Read `project_state.json` and `literature/search_log.md`.\n"
        "2. Search only English scholarly sources, DOI records, CrossRef, "
        "OpenAlex, arXiv, Semantic Scholar, or publisher pages.\n"
        "3. Add candidate updates to `task_queue.md`; do not edit `refs.bib` "
        "without a citation verification step.\n"
        "4. Refresh `project_state.json` with `update_workspace_state.py`.\n\n"
        "## Reviewer Feedback Check\n\n"
        "1. Read `decision_log.md`, `task_queue.md`, and available reviewer notes.\n"
        "2. Convert new feedback into actionable tasks with location, evidence, "
        "and completion criteria.\n"
        "3. Draft any reply text for author review; do not send it.\n"
        "4. Refresh `project_state.json` with `update_workspace_state.py`.\n\n"
        "## Blocking Item Summary\n\n"
        "1. Read `project_state.json` and list `blocking_items`.\n"
        "2. Group blockers by author input, external data, failed audit, or "
        "missing artifact.\n"
        "3. Update `task_queue.md` with the smallest next action for each blocker.\n"
        "4. Refresh `project_state.json` with `update_workspace_state.py`.\n"
    )


def control_file_defaults(workspace: Path) -> dict[str, str]:
    return {
        "project_state.json": json.dumps(default_project_state(workspace), indent=2, ensure_ascii=False) + "\n",
        "decision_log.md": default_decision_log(),
        "task_queue.md": default_task_queue(),
        "artifact_index.json": json.dumps(default_artifact_index(), indent=2, ensure_ascii=False) + "\n",
        "automation_recipes.md": default_automation_recipes(),
    }


def init_control_files(workspace: Path, overwrite: bool = False) -> dict:
    workspace.mkdir(parents=True, exist_ok=True)
    created: list[str] = []
    existing: list[str] = []
    overwritten: list[str] = []
    for rel, content in control_file_defaults(workspace).items():
        path = workspace / rel
        if path.exists() and not overwrite:
            existing.append(rel)
            continue
        if path.exists():
            overwritten.append(rel)
        else:
            created.append(rel)
        path.write_text(content, encoding="utf-8")
    return {
        "control_files_created": created,
        "control_files_existing": existing,
        "control_files_overwritten": overwritten,
    }


def copy_if_exists(src: Path, dst: Path, overwrite: bool) -> bool:
    if not src.exists():
        return False
    if dst.exists() and not overwrite:
        return True
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return True


def copy_tree_files(src_dir: Path, dst_dir: Path, overwrite: bool) -> int:
    if not src_dir.exists():
        return 0
    count = 0
    for path in sorted(src_dir.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(src_dir)
        target = dst_dir / rel
        if target.exists() and not overwrite:
            count += 1
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
        count += 1
    return count


def first_existing(paths: list[Path]) -> Path | None:
    for path in paths:
        if path.exists():
            return path
    return None


def init_workspace(source: Path, workspace: Path, overwrite: bool) -> dict:
    workspace.mkdir(parents=True, exist_ok=True)
    for rel in DIRS:
        (workspace / rel).mkdir(parents=True, exist_ok=True)

    old_inputs = source / "paper_orchestra_workspace" / "inputs"
    copied: dict[str, str] = {}

    input_map = {
        "idea.md": [
            old_inputs / "idea.md",
            source / "idea.md",
            source / "PAPER_POSITIONING_MATERIAL_CN.md",
        ],
        "experimental_log.md": [
            old_inputs / "experimental_log_revision_addendum.md",
            old_inputs / "experimental_log.md",
            source / "EXPERIMENT_REPORT_CLEAN_CN.md",
        ],
        "template.tex": [
            source / "template.tex",
            old_inputs / "template.tex",
        ],
        "conference_guidelines.md": [
            source / "conference_guidelines_Applied_Energy.md",
            old_inputs / "conference_guidelines.md",
        ],
    }

    for name, candidates in input_map.items():
        src = first_existing(candidates)
        if src and copy_if_exists(src, workspace / "inputs" / name, overwrite):
            copied[name] = str(src)

    for name in SOURCE_MATERIALS:
        src = source / name
        if copy_if_exists(src, workspace / "inputs" / "source_materials" / name, overwrite):
            copied[f"source_materials/{name}"] = str(src)

    figure_count = 0
    for fig_dir in [
        source / "figures",
        old_inputs / "figures",
        source / "paper_orchestra_workspace" / "figures",
    ]:
        figure_count += copy_tree_files(fig_dir, workspace / "inputs" / "figures", overwrite)

    profile_path = workspace / "workflow_profile.json"
    if overwrite or not profile_path.exists():
        guideline_name = copied.get("conference_guidelines.md", "")
        journal = "applied-energy" if "Applied_Energy" in guideline_name or "Applied Energy" in guideline_name else ""
        profile = {
            "paper_type": "research",
            "topics": [],
            "journal": journal,
            "paper_type_confidence": 0.6,
            "topic_confidence": {},
            "journal_confidence": 0.8 if journal else 0.0,
            "profile_source": "init_workspace default",
            "routing_notes": [
                "Default profile created from available inputs. Confirm topics before loading topic-specific fragments."
            ],
            "loaded_fragments": [],
            "disabled_fragments": [],
            "quality_thresholds": {},
        }
        if journal == "applied-energy":
            profile["loaded_fragments"].append("_shared/fragments/journal/applied-energy.md")
        profile_path.write_text(json.dumps(profile, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    control_status = init_control_files(workspace, overwrite=overwrite)

    status = {
        "created_at": utc_now(),
        "source": str(source),
        "workspace": str(workspace),
        "copied": copied,
        "figure_files_seen": figure_count,
        "profile": str(profile_path),
        **control_status,
        "status": "PASS",
    }
    (workspace / "orchestrator_status.json").write_text(
        json.dumps(status, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return status


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", help="Experiment source folder")
    parser.add_argument(
        "--workspace",
        help="Workspace path. Defaults to SOURCE/mechanism_paper_workspace",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite copied input files if they already exist",
    )
    parser.add_argument(
        "--init-missing",
        action="store_true",
        help="Only create missing workbench control files in an existing workspace",
    )
    args = parser.parse_args()

    source = Path(args.source).resolve() if args.source else None
    if args.init_missing:
        if args.workspace:
            workspace = Path(args.workspace).resolve()
        elif source:
            workspace = source / "mechanism_paper_workspace"
        else:
            print(json.dumps({"status": "FAIL", "error": "--init-missing requires --workspace or --source"}, indent=2))
            return 1
        status = {
            "created_at": utc_now(),
            "workspace": str(workspace),
            **init_control_files(workspace, overwrite=False),
            "status": "PASS",
        }
        print(json.dumps(status, indent=2, ensure_ascii=False))
        return 0

    if source is None:
        print(json.dumps({"status": "FAIL", "error": "--source is required unless --init-missing is used"}, indent=2))
        return 1

    workspace = Path(args.workspace).resolve() if args.workspace else source / "mechanism_paper_workspace"
    if not source.exists():
        print(json.dumps({"status": "FAIL", "error": f"source not found: {source}"}, indent=2))
        return 1

    status = init_workspace(source, workspace, args.overwrite)
    print(json.dumps(status, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
