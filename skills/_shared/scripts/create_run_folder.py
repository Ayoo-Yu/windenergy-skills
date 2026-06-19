#!/usr/bin/env python3
"""Create a per-invocation output folder for renewable skills."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9._-]+", "-", value)
    value = re.sub(r"-+", "-", value)
    return value.strip("-") or "run"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", default=".")
    parser.add_argument("--output-root")
    parser.add_argument("--skill", required=True)
    parser.add_argument("--target", default="general")
    parser.add_argument("--timestamp")
    args = parser.parse_args()

    source_dir = Path(args.source_dir).resolve()
    root = Path(args.output_root).resolve() if args.output_root else source_dir / "skill_runs"
    stamp = args.timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    name = f"{stamp}_{slugify(args.skill)}_{slugify(args.target)}"
    run_dir = root / name
    run_dir.mkdir(parents=True, exist_ok=False)

    manifest_path = run_dir / "RUN_MANIFEST.md"
    manifest_path.write_text(
        "\n".join(
            [
                "# Run Manifest",
                "",
                f"- Skill: {args.skill}",
                f"- Timestamp: {stamp}",
                f"- Source directory: {source_dir}",
                f"- Target or mode: {args.target}",
                "",
                "## Input Files",
                "",
                "- AUTHOR_INPUT_NEEDED",
                "",
                "## Generated Files",
                "",
                "- AUTHOR_INPUT_NEEDED",
                "",
                "## Manual Author Decisions",
                "",
                "- AUTHOR_INPUT_NEEDED",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(json.dumps({"run_dir": str(run_dir), "manifest_path": str(manifest_path)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

