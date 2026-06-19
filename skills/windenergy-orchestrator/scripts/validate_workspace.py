#!/usr/bin/env python3
"""Validate windenergy-orchestrator workspace inputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_DIRS = [
    "inputs",
    "inputs/figures",
    "diagnostics",
    "outline",
    "literature",
    "figures",
    "drafts",
    "refinement",
    "audits",
    "final",
]

REQUIRED_FILES = [
    "workflow_profile.json",
    "inputs/idea.md",
    "inputs/experimental_log.md",
    "inputs/template.tex",
    "inputs/conference_guidelines.md",
]

TEXT_SUFFIXES = {".md", ".tex", ".json", ".bib", ".txt"}
FIGURE_SUFFIXES = {".png", ".pdf", ".jpg", ".jpeg", ".svg"}
PROFILE_FIELDS = {
    "paper_type",
    "topics",
    "journal",
    "paper_type_confidence",
    "topic_confidence",
    "journal_confidence",
    "profile_source",
    "routing_notes",
    "loaded_fragments",
    "disabled_fragments",
    "quality_thresholds",
}


def read_utf8(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validate_workspace(workspace: Path) -> dict:
    checks: list[dict] = []
    warnings: list[str] = []

    if not workspace.exists():
        return {
            "workspace": str(workspace),
            "status": "FAIL",
            "checks": [{"path": str(workspace), "status": "FAIL", "reason": "workspace missing"}],
            "warnings": warnings,
        }

    for rel in REQUIRED_DIRS:
        path = workspace / rel
        checks.append(
            {
                "path": rel,
                "status": "PASS" if path.is_dir() else "FAIL",
                "reason": "directory exists" if path.is_dir() else "directory missing",
            }
        )

    for rel in REQUIRED_FILES:
        path = workspace / rel
        if not path.exists():
            checks.append({"path": rel, "status": "FAIL", "reason": "file missing"})
            continue
        try:
            text = read_utf8(path)
        except UnicodeDecodeError:
            checks.append({"path": rel, "status": "FAIL", "reason": "not valid UTF-8"})
            continue
        status = "PASS"
        reason = "valid UTF-8"
        if rel.endswith("template.tex") and "\\begin{document}" not in text:
            status = "FAIL"
            reason = "template lacks LaTeX document body"
        if rel.endswith("conference_guidelines.md") and not text.strip():
            status = "FAIL"
            reason = "guidelines empty"
        if rel.endswith("workflow_profile.json"):
            try:
                profile = json.loads(text)
            except json.JSONDecodeError:
                status = "FAIL"
                reason = "invalid workflow profile JSON"
            else:
                missing_fields = sorted(PROFILE_FIELDS - set(profile if isinstance(profile, dict) else {}))
                if missing_fields:
                    status = "FAIL"
                    reason = "profile missing fields: " + ", ".join(missing_fields)
        checks.append({"path": rel, "status": status, "reason": reason})

    figures = [
        path
        for path in (workspace / "inputs" / "figures").rglob("*")
        if path.is_file() and path.suffix.lower() in FIGURE_SUFFIXES
    ]
    checks.append(
        {
            "path": "inputs/figures",
            "status": "PASS" if figures else "UNCHECKED",
            "reason": f"{len(figures)} figure files found" if figures else "no figure files found",
        }
    )

    for path in workspace.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            read_utf8(path)
        except UnicodeDecodeError:
            checks.append(
                {
                    "path": str(path.relative_to(workspace)),
                    "status": "FAIL",
                    "reason": "not valid UTF-8",
                }
            )

    statuses = {item["status"] for item in checks}
    if "FAIL" in statuses:
        status = "FAIL"
    elif "UNCHECKED" in statuses:
        status = "UNCHECKED"
    else:
        status = "PASS"

    return {
        "workspace": str(workspace),
        "status": status,
        "checks": checks,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace")
    parser.add_argument("--json-output", help="Optional path to write JSON report")
    args = parser.parse_args()

    report = validate_workspace(Path(args.workspace).resolve())
    text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.json_output:
        Path(args.json_output).write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if report["status"] in {"PASS", "UNCHECKED"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
