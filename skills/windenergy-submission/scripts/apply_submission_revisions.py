#!/usr/bin/env python3
"""Apply tracked revisions to multiple submission documents.

Usage:
    python apply_submission_revisions.py PLAN.json

Plan JSON:
{
  "source_dir": "D:/papers/RE0530",
  "output_dir": "D:/papers/RE0530/skill_runs/20260531-153012_windenergy-submission_renewable-energy",
  "color_crossrefs": true,
  "jobs": [
    {
      "input": "Cover Letter.docx",
      "changes": [
        {
          "paragraph_index": 19,
          "old": "Thank you ... reconsideration ...",
          "new": "Thank you ... consideration ...",
          "note": "fresh submission wording"
        }
      ],
      "output": "Cover Letter_submission_tracked.docx"
    }
  ]
}
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parents[1]
POLISHER_DIR = ROOT / "windenergy-polishing" / "scripts"
sys.path.insert(0, str(POLISHER_DIR))

from polish_docx import BLUE, TrackedPolisher, validate_tracked_changes  # noqa: E402


def resolve_input(value: str, source_dir: Path) -> Path:
    path = Path(value)
    return path.resolve() if path.is_absolute() else (source_dir / path).resolve()


def resolve_output(value: str | None, input_path: Path, output_dir: Path | None) -> Path:
    default_name = f"{input_path.stem}_submission_tracked{input_path.suffix}"
    if value:
        path = Path(value)
        if path.is_absolute():
            return path.resolve()
        base = output_dir if output_dir else input_path.parent
        return (base / path).resolve()
    base = output_dir if output_dir else input_path.parent
    return (base / default_name).resolve()


def apply_job(job: dict, source_dir: Path, output_dir: Path | None, color_default: bool) -> dict:
    input_path = resolve_input(job["input"], source_dir)
    output_path = resolve_output(job.get("output"), input_path, output_dir)
    changes = job.get("changes", [])

    if not input_path.exists():
        return {
            "input": str(input_path),
            "output": str(output_path),
            "applied": [],
            "not_applied": [{"reason": "input file not found"}],
            "validation": {},
        }

    polisher = TrackedPolisher(input_path)
    applied, not_applied = polisher.apply_all(changes)
    color_crossrefs = bool(job.get("color_crossrefs", color_default))
    color_result = {}
    if color_crossrefs:
        color_result = polisher.color_crossrefs(str(job.get("crossref_color", BLUE)))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    polisher.save(output_path)
    validation = validate_tracked_changes(output_path)

    return {
        "input": str(input_path),
        "output": str(output_path),
        "applied": applied,
        "not_applied": not_applied,
        "formatting": color_result,
        "validation": validation,
    }


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: apply_submission_revisions.py PLAN.json")
        return 1

    plan_path = Path(sys.argv[1]).resolve()
    with plan_path.open("r", encoding="utf-8") as handle:
        plan = json.load(handle)

    source_dir = Path(plan.get("source_dir", plan_path.parent)).resolve()
    output_dir = Path(plan["output_dir"]).resolve() if plan.get("output_dir") else None
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)

    color_default = bool(plan.get("color_crossrefs", False))
    results = [apply_job(job, source_dir, output_dir, color_default) for job in plan.get("jobs", [])]

    print(json.dumps({"results": results}, ensure_ascii=False, indent=2))

    failed = any(result["not_applied"] for result in results)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
