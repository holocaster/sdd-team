#!/usr/bin/env bash
# Regenerates .opencode/agents/*.md from .claude/agents/*.md.
# Claude frontmatter (name/tools) differs from opencode's (mode/permissions),
# so the body is copied but the frontmatter is rebuilt per agent below.
# Run this after editing a .claude/agents/*.md body or description.
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
claude_dir="$repo_root/.claude/agents"
opencode_dir="$repo_root/.opencode/agents"

sync_agent() {
  local name="$1"
  local extra_frontmatter="$2"
  local src="$claude_dir/$name.md"
  local dst="$opencode_dir/$name.md"

  local description
  description="$(grep '^description:' "$src" | head -1 | sed 's/^description: //')"

  local body
  body="$(awk 'BEGIN{n=0} /^---$/{n++; next} n>=2{print}' "$src")"

  {
    echo "---"
    echo "description: $description"
    echo "mode: subagent"
    if [[ -n "$extra_frontmatter" ]]; then
      printf '%s\n' "$extra_frontmatter"
    fi
    echo "---"
    printf '%s\n' "$body"
  } > "$dst"

  echo "synced $name"
}

sync_agent "sdd-implementer" ""
sync_agent "sdd-planner" ""
sync_agent "sdd-reviewer" "$(printf 'permissions:\n  - action: edit\n    resource: "*"\n    effect: deny')"
