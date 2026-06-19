#!/usr/bin/env python3
"""List long supported text blocks in a docx manuscript.

Usage:
    python scan_docx_blocks.py Manuscript.docx --min-words 80
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parents[1]
POLISHER_DIR = ROOT / "windenergy-polishing" / "scripts"
sys.path.insert(0, str(POLISHER_DIR))

from polish_docx import TrackedPolisher  # noqa: E402


WORD_RE = re.compile(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?")


def word_count(text: str) -> int:
    return len(WORD_RE.findall(text))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("docx")
    parser.add_argument("--min-words", type=int, default=80)
    args = parser.parse_args()

    path = Path(args.docx)
    if not path.exists():
        print(f"Input file not found: {path}", file=sys.stderr)
        return 1

    polisher = TrackedPolisher(path)
    rows = []
    for block in polisher.blocks:
        text = block.text.strip()
        count = word_count(text)
        if count >= args.min_words:
            rows.append(
                {
                    "block_id": block.block_id,
                    "kind": block.kind,
                    "words": count,
                    "preview": text[:260],
                }
            )
    rows.sort(key=lambda item: item["words"], reverse=True)
    print(json.dumps(rows, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
