#!/usr/bin/env bash
# Package each skill into a zip file under dist/ for easy import into Claude Desktop.
#
# Usage:
#   ./scripts/build_dist.sh

set -euo pipefail

ROOT="$(unset CDPATH; cd "$(dirname "$0")/.." && pwd)"
SKILLS_DIR="$ROOT/skills"
DIST_DIR="$ROOT/dist"

rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"

count=0
for skill_dir in "$SKILLS_DIR"/*/; do
    skill_name="$(basename "$skill_dir")"
    zip_file="$DIST_DIR/$skill_name.zip"

    # Create a clean copy excluding .git dirs and gitignored files
    tmp_dir="$(mktemp -d)"
    trap 'rm -rf "$tmp_dir"' EXIT

    # Use git archive if the skill contains a git repo with a .gitignore,
    # otherwise fall back to rsync excluding .git directories.
    gitignore_files=()
    while IFS= read -r -d '' gi; do
        gitignore_files+=("$gi")
    done < <(find "$skill_dir" -name .gitignore -print0 2>/dev/null)

    if [[ ${#gitignore_files[@]} -gt 0 ]]; then
        # Build rsync filter rules from each .gitignore
        filter_args=(--exclude='.git')
        for gi in "${gitignore_files[@]}"; do
            gi_dir="$(dirname "$gi")"
            gi_rel="${gi_dir#"$skill_dir"}"
            # Read each .gitignore and add exclude rules with the correct path prefix
            while IFS= read -r line; do
                # Skip comments and empty lines
                [[ -z "$line" || "$line" == \#* ]] && continue
                # Skip negation patterns (lines starting with !)
                [[ "$line" == \!* ]] && continue
                # Strip leading slash (makes it relative to the .gitignore location)
                pattern="${line#/}"
                if [[ -n "$gi_rel" ]]; then
                    filter_args+=(--exclude="$gi_rel/$pattern")
                else
                    filter_args+=(--exclude="$pattern")
                fi
            done < "$gi"
        done
        rsync -a "${filter_args[@]}" "$skill_dir" "$tmp_dir/$skill_name/"
    else
        rsync -a --exclude='.git' "$skill_dir" "$tmp_dir/$skill_name/"
    fi

    (cd "$tmp_dir" && zip -qr "$zip_file" "$skill_name")
    rm -rf "$tmp_dir"

    echo "  $skill_name.zip"
    count=$((count + 1))
done

if [[ $count -eq 0 ]]; then
    echo "No skills found."
else
    echo ""
    echo "Done — $count skill(s) packaged in dist/"
fi
