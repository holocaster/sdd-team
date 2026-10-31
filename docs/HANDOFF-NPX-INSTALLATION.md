# Handoff: npx installation and first-run permissions

Date: 2026-10-03
Updated: 2026-10-29
Status: artifact-only bootstrap implemented; installer and permission opt-in deferred.

## Next-session objective

Prepare **sdd-team** for public installation through `npx`, with transparent setup
and an explicit first-run choice about autonomous execution. Discuss the open
decisions with the user before implementing the installer or permission setup.

The repository is [holocaster/sdd-team](https://github.com/holocaster/sdd-team).
Use `sdd-team` as the project and package identity; local checkout folder names
are not installation paths or product names.

## Current state and references

- [README.md](../README.md) describes prerequisites, skill installation, manual
  agent registration, the workflow, and optional Ponytail integration.
- [AGENTS.md](../AGENTS.md) defines maintenance rules. `CLAUDE.md` is its relative
  symlink. This repository distributes the workflow; it does not run SDD on itself.
- [SYNC.md](../.claude/skills/SYNC.md) records the deliberate upstream forks.
- [sdd-main](../.claude/skills/sdd-main/SKILL.md) owns initialization and orchestration.
- [bootstrap.sh](../.claude/skills/sdd-main/bootstrap.sh) creates only project
  artifacts and preserves all client permission settings. Automatic permission
  setup, consent and client detection remain unimplemented. Previously generated
  settings are preserved too; this change does not revoke existing permissions.
- [Script checks](../tests/test_scripts.py) cover initialization without permission
  changes, existing files, repeated runs and profile synchronization. The
  [CI workflow](../.github/workflows/checks.yml) runs them on pushes and pull requests.
- The [reviewer](../.claude/agents/sdd-reviewer.md) now requires
  [BRANCH security review](../.claude/skills/sdd-security-review/SKILL.md) for each
  ticket or Batch. This integration was committed as `fa87616`.
- There is no npm installer or root `package.json` yet. The local `.opencode`
  dependency files are ignored harness artifacts, not a distributable installer.

Existing global symlinks used for development are not a public installation
contract. Installed copies need an update mechanism; installed symlinks need a
stable destination that remains available after the `npx` process exits.

## Requirements agreed with the user

1. Users must be able to install the agents and skills through an `npx` entrypoint.
2. Installation must explain what it installs, where it writes, and which
   dependencies are required. It must not silently enable autonomous execution.
3. On the first run of `sdd-main` in a target repository, ask whether the user wants
   the permissions needed to avoid repeated execution approvals.
4. Only an explicit **yes** authorizes changing permissions. A no or unanswered
   question leaves the user's permission settings intact; SDD can still initialize
   its artifacts and operate with ordinary approvals.
5. Optional permission setup must identify the active client: **Claude Code, Codex,
   or opencode**, and apply the corresponding configuration only after consent.
   Artifact-only bootstrap runs independently of that setup.
6. Preserve existing settings and restrictions. Explain any remaining approvals
   caused by sandbox boundaries, explicit restrictions, or managed policy.
7. Keep the SDD role boundaries: independent review, exact commit ranges,
   committed handoffs, and serial implementation remain authoritative.
8. Decisions about product behavior, scope, and workflow blockers still go through
   Main. Permission consent is not approval of every future product decision.

## Proposed first-run experience

This is a proposal to discuss, not an implemented interface:

> Enable autonomous execution for this repository in <client>?
> This configures routine file edits, shell commands, local commits, and SDD
> delegation to run without repeated approval prompts. Shell commands may use
> your account's access; a project setting is not itself a filesystem sandbox.
>
> Enable autonomous execution / Keep current permissions

- Main presents the choice through the client's user-question interface. A shell
  script launched by an agent may not have an interactive terminal.
- Main passes the accepted choice and client identity explicitly to the separate
  permission setup. A missing argument must not be interpreted as consent.
- Remember the choice locally per user, target repository, and client. A committed
  `PROJECT_STATE.md`, shared config, or teammate's prior consent must not authorize
  changes for another user. A declined choice should not cause repeated prompts.
- Show the configuration changes and how to revoke them. If already configured,
  avoid rewriting or asking again unnecessarily.
- A later installation update must not expand permissions under old consent.

## Client-specific starting points

Verify the installed client version and current official documentation before
writing configuration. These systems do not share one permission schema.

| Client | Repository-scoped setup to investigate | Important distinction |
|---|---|---|
| Claude Code | `.claude/settings.local.json` | Local consent should not be distributed in shared settings. Check current `Agent` tool rules rather than assuming legacy `Task` names. |
| Codex | `.codex/config.toml` and `.codex/rules/*.rules` | Project layers require trust. Approval policy and sandbox access are separate; command rules can preapprove selected outside-sandbox execution. |
| opencode | `opencode.jsonc` or `.opencode/opencode.jsonc` | V2 uses ordered `permissions` rules with `shell` and `subagent`; V1 uses different fields. Preserve agent-specific restrictions. |

Global alternatives exist under `~/.claude`, `~/.codex`, and
`~/.config/opencode`, but repository-local permission setup is the proposed default.
Any global permission change requires its own explicit choice.

Official sources consulted:

- [Claude Code permissions](https://code.claude.com/docs/en/permissions)
- [Codex configuration](https://developers.openai.com/codex/config-file/config-basic)
- [Codex command rules](https://developers.openai.com/codex/agent-configuration/rules)
- [Codex sandbox and approvals](https://developers.openai.com/codex/agent-approvals-security)
- [opencode V2 configuration](https://opencode.ai/v2/docs/config)
- [opencode V2 permissions](https://opencode.ai/v2/docs/permissions)
- [skills CLI](https://github.com/vercel-labs/skills)
- [npm public registry](https://docs.npmjs.com/about-the-public-npm-registry)

## Open decisions for the next session

- Package name and CLI commands. `@holocaster/sdd-team` is an example, not a
  published package or a verified available npm scope.
- Whether to reuse `skills` for skill installation or ship a self-contained
  installer that installs both skills and agent registrations.
- How to package or install external skills (`grilling`, `domain-modeling`, `tdd`
  and their dependencies) and check Gitleaks availability.
- Reliable client detection. Prefer an explicit caller identity or override;
  identify verified detection signals and ask when ambiguous. The existence of
  `.claude/`, `.codex/`, or `.opencode/` does not establish the active client.
- Where to remember yes/no locally, how to reconfigure, and how to revoke only
  the settings introduced by this setup.
- The exact autonomous permission set per client: broad shell access versus
  specific commands, network needs, protected Git paths, and temporary scan files.
  `approval_policy = "never"` alone does not grant Codex sandbox access.
- How to preserve JSON/JSONC/TOML settings and handle existing incompatible rules.
- Whether configuration changes apply immediately or require a new session.
- Supported client versions and the project/global installation options.

## Suggested implementation sequence after decisions

1. Agree on the installation and consent experience; define scope and versions.
2. Keep artifact-only initialization and implement separate opt-in permission
   setup, coordinated by `sdd-main`, with reliable client identification.
3. Check fresh and existing configurations for yes, no, unanswered/non-interactive,
   repeat-run, and ambiguous-client scenarios in temporary test repositories.
4. Verify representative SDD work: edits, delegation, tests, local commits,
   BRANCH credential scanning, and retained reviewer restrictions.
5. Add the minimal npm CLI, package the required artifacts, and test the packed
   installer in fresh environments without relying on this machine's symlinks.
6. Update public installation documentation to match the implemented behavior.
   Publish to npm only after package identity and publishing access are confirmed.

## Suggested skills

- `writing-for-agents` and `writing-great-skills` for Main and profile changes.
- `deep-analyse` for version-specific client configuration and npm behavior.
- `customize-opencode` when editing opencode configuration or agent integration.
- `ponytail` for the smallest installer and bootstrap implementation that meets
  the agreed requirements, if its policy is not already injected by the harness.

Follow [AGENTS.md](../AGENTS.md) for canonical/generated sources and verification.
Artifact-only bootstrap and its script checks are implemented. The installer and
permission opt-in remain future work; their next session starts with the open
decisions above.
