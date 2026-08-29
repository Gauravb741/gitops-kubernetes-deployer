#!/usr/bin/env bash
# ── fix-newlines.sh ───────────────────────────────────────────────────────────
# Ensures every YAML file in the repository ends with a newline character.
# Run once locally before committing: bash scripts/fix-newlines.sh
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

GREEN='\033[0;32m'; BLUE='\033[0;34m'; NC='\033[0m'

fixed=0
checked=0

while IFS= read -r -d '' file; do
  checked=$((checked + 1))
  # Check if file is missing a trailing newline
  if [ -s "$file" ] && [ "$(tail -c 1 "$file" | wc -l)" -eq 0 ]; then
    echo -e "${BLUE}[FIX]${NC}  Adding trailing newline: $file"
    echo "" >> "$file"
    fixed=$((fixed + 1))
  fi
done < <(find . \
  -not -path './.git/*' \
  -not -path './venv/*' \
  -not -path './.venv/*' \
  \( -name "*.yaml" -o -name "*.yml" \) \
  -print0)

echo -e "${GREEN}[DONE]${NC} Checked: $checked files | Fixed: $fixed files"