# sdd-team

Canonical source for the SDD (spec-driven development) workflow: the `sdd-main`
skill and isolated planner/implementer/reviewer profiles for target repositories.
Installation registers skills and agents; `bootstrap.sh` initializes a target
project's artifacts. This repo does not run the workflow on itself and has no
`.ai/PROJECT_STATE.md`.

## Source of truth

- `.claude/skills/sdd-main/SKILL.md` and `.claude/agents/sdd-*.md` define the
  actual workflow semantics - handoff contracts, phases, Batch rules.
  Everything else derives from them.
- `.opencode/agents/sdd-*.md` is generated, never hand-edited. After changing
  a `.claude/agents/*.md` body or description, run `.opencode/sync-agents.sh`
  before committing, or the opencode copy silently goes stale.
- `.claude/skills/SYNC.md` identifies the deliberate Matt Pocock skill forks
  and their differences. Read it before reconciling a fork against upstream;
  a blind re-copy breaks the SDD flow. `sdd-main` and `sdd-security-review`
  are separate workflow skills, not part of that fork inventory.
- `README.md` documents installation, prerequisites, and the workflow overview.
  Read it and the relevant canonical skills/profiles before changing behavior.
- `docs/archive/` contains historical research, not current workflow instructions.

## Editing this repo

- `CLAUDE.md` is a relative symlink to `AGENTS.md`; edit this file to update both.
- Preserve role isolation, exact review ranges, and committed handoff contracts.
- After a profile change, run `.opencode/sync-agents.sh` and verify generated
  profiles match their canonical bodies. Check documentation changes with
  `git diff --check` and verify local links resolve.
- Contributors may symlink installed skills and agents to this checkout. In that
  setup, edits affect every project using those links immediately. Copies require
  an installation update.
