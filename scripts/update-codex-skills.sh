#!/usr/bin/env bash
#
# 将 windenergy-skills 安装或更新到 Codex skills 目录。
# 仅同步本仓库 skills/ 下的目录，不处理其他已安装技能。
#
# 用法：
#   scripts/update-codex-skills.sh
#   PULL=1 scripts/update-codex-skills.sh
#   CODEX_SKILLS_DIR=/path/to/skills scripts/update-codex-skills.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SRC="$REPO_ROOT/skills"
DST="${CODEX_SKILLS_DIR:-$HOME/.codex/skills}"

if [ ! -d "$SRC" ]; then
  echo "error: skills directory not found at $SRC" >&2
  exit 1
fi

# 可选：安装前拉取最新提交。
if [ "${PULL:-0}" = "1" ] && git -C "$REPO_ROOT" rev-parse --git-dir >/dev/null 2>&1; then
  echo "==> Pulling latest"
  git -C "$REPO_ROOT" pull --ff-only
fi

if ! command -v rsync >/dev/null 2>&1; then
  echo "error: rsync is required but not installed" >&2
  exit 1
fi

mkdir -p "$DST"
echo "==> Syncing skills from $SRC"
echo "    into $DST"
for path in "$SRC"/*/; do
  d="$(basename "$path")"
  mkdir -p "$DST/$d"
  rsync -a --delete "$path" "$DST/$d/"
  echo "    copied $d"
done

echo "==> Done"
