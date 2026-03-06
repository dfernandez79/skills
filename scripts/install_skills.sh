#!/usr/bin/env bash
# Install each skill into ~/.claude/skills/ for use with Claude Code.
# Existing skills are replaced with the latest version.
# Files matched by .gitignore in each skill directory are excluded.
#
# Usage:
#   ./scripts/install_skills.sh

set -euo pipefail

ROOT="$(unset CDPATH; cd "$(dirname "$0")/.." && pwd)"
SKILLS_DIR="$ROOT/skills"
TARGET_DIR="$HOME/.claude/skills"

mkdir -p "$TARGET_DIR"

count=0
for skill_dir in "$SKILLS_DIR"/*/; do
    skill_name="$(basename "$skill_dir")"
    dest="$TARGET_DIR/$skill_name"

    # Remove existing version if present
    if [[ -d "$dest" ]]; then
        rm -rf "$dest"
    fi

    # Build rsync filter rules from any .gitignore files in the skill
    gitignore_files=()
    while IFS= read -r -d '' gi; do
        gitignore_files+=("$gi")
    done < <(find "$skill_dir" -name .gitignore -print0 2>/dev/null)

    filter_args=(--exclude='.git')
    if [[ ${#gitignore_files[@]} -gt 0 ]]; then
        for gi in "${gitignore_files[@]}"; do
            gi_dir="$(dirname "$gi")"
            gi_rel="${gi_dir#"$skill_dir"}"
            while IFS= read -r line; do
                [[ -z "$line" || "$line" == \#* ]] && continue
                [[ "$line" == \!* ]] && continue
                pattern="${line#/}"
                if [[ -n "$gi_rel" ]]; then
                    filter_args+=(--exclude="$gi_rel/$pattern")
                else
                    filter_args+=(--exclude="$pattern")
                fi
            done < "$gi"
        done
    fi

    rsync -a "${filter_args[@]}" "$skill_dir" "$dest/"

    echo "  $skill_name -> $dest"
    count=$((count + 1))
done

if [[ $count -eq 0 ]]; then
    echo "No skills found."
else
    echo ""
    echo "Done — $count skill(s) installed to $TARGET_DIR"
fi
