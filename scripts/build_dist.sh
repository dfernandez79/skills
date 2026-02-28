#!/usr/bin/env bash
# Package each skill into a zip file under dist/ for easy import into Claude Desktop.
#
# Usage:
#   ./scripts/build_dist.sh

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILLS_DIR="$ROOT/skills"
DIST_DIR="$ROOT/dist"

rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"

count=0
for skill_dir in "$SKILLS_DIR"/*/; do
    skill_name="$(basename "$skill_dir")"
    zip_file="$DIST_DIR/$skill_name.zip"
    (cd "$SKILLS_DIR" && zip -qr "$zip_file" "$skill_name")
    echo "  $skill_name.zip"
    count=$((count + 1))
done

if [[ $count -eq 0 ]]; then
    echo "No skills found."
else
    echo ""
    echo "Done — $count skill(s) packaged in dist/"
fi
