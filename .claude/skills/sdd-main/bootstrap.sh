#!/usr/bin/env bash
set -euo pipefail

if ! git rev-parse --git-dir >/dev/null 2>&1; then
  echo "warning: not a git repo - run 'git init' and create a feature branch first" >&2
fi

branch="$(git branch --show-current 2>/dev/null || true)"
case "$branch" in
  main|master|"") echo "warning: on '$branch' - create a feature branch before running the workflow" >&2 ;;
esac

mkdir -p .ai docs/briefs docs/specs docs/adrs tickets

if [ ! -f docs/CONTEXT.md ]; then
  cat > docs/CONTEXT.md <<'EOF'
# <project>

<one line: what this project is>

## Language

<glossary - filled during discovery>

## Decisions

<cross-cutting decisions - filled during discovery, each linked to its ADR>
EOF
fi

if [ ! -f .ai/PROJECT_STATE.md ]; then
  cat > .ai/PROJECT_STATE.md <<'EOF'
goal: null
feature: null
context: docs/CONTEXT.md
brief: null
spec: null
tickets_index: null
active_ticket: null
base_sha: null
head_sha: null
review: null
review_round: 0
blockers: []
next_action: run sizing / discovery for the current request
EOF
fi

echo "Bootstrap done."
echo "  .ai/PROJECT_STATE.md, docs/, tickets/  - artifact skeleton"
echo "Client permission settings are unchanged."
echo "Commit these, then invoke the main / sdd-main agent."
