---
name: sdd-code-review
description: Two-axis (Standards + Spec) review of an exact commit range, for the isolated sdd-reviewer subagent. Deliberate fork of code-review (see .claude/skills/SYNC.md) - takes an explicit base..head range instead of HEAD, needs no issue tracker, and runs the two axes in sequence because a subagent cannot spawn sub-agents.
---

Two-axis review of `git diff <base_sha>..<head_sha>` - the exact range the caller gives you, not `HEAD`:

- **Standards**: does the code conform to this repo's documented coding standards?
- **Spec**: does the code faithfully implement the ticket / spec the caller names?

The caller (`sdd-reviewer`) passes `base_sha`, `head_sha`, the spec/ticket reference, and sanitized context paths and source mappings from its preceding BRANCH security pass. There is no issue tracker step and no `/setup-matt-pocock-skills` dependency.

## Process

### 1. Pin the range

Confirm both SHAs resolve (`git rev-parse`) and the supplied sanitized diff/log represent exactly `base_sha..head_sha` (two-dot; this workflow runs one linear branch). Use the supplied snapshots for source reads and searches throughout this review, preserving original paths and line numbers; do not emit raw diff/log or substitute checkout files. If sanitized context is missing or does not match the range, report a blocker to the caller. Disregard changes to `.ai/**` and `tickets/**` non-code files (`index.md`, `*.review.md`) inside the range - orchestration bookkeeping the orchestrator committed, not the implementation. An empty implementation diff does not invalidate the preceding credential scan of selected commits.

### 2. Spec source

The caller names it: `docs/specs/<NNNN-slug>.md` (section refs), or - on a fast-path ticket - the ticket's own "What to build" and acceptance criteria. If neither is available, do the Spec axis as "no spec available" and say so.

### 3. Standards sources

Search the repo for every file that documents how code should be written. When `CODING_STANDARDS.md`, `CONTRIBUTING.md` or `CLAUDE.md` exists, it must be on the list. On top of that, always apply the **smell baseline**: the Fowler code smells (_Refactoring_ ch.3) - Mysterious Name, Duplicated Code, Feature Envy, Data Clumps, Primitive Obsession, Repeated Switches, Shotgun Surgery, Divergent Change, Speculative Generality, Message Chains, Middle Man, Refused Bequest. Each is a judgement call ("possible Feature Envy"), never a hard violation. A documented repo standard overrides the baseline; skip anything tooling already enforces.

### 4. Run both axes (in sequence)

You are a subagent and cannot spawn sub-agents, so run the two axes one after the other, keeping their findings separate.

- **Standards**: per file/hunk, (a) every place the diff breaks a documented standard - cite the standard; (b) any baseline smell - name it, quote the hunk. Hard violations vs judgement calls.
- **Spec**: (a) requirements asked for but missing or partial; (b) behaviour not asked for (scope creep); (c) requirements that look implemented but wrong. Quote the spec / acceptance-criterion line per finding.

### 5. Aggregate

Report under `## Standards` and `## Spec` headings. Do not merge or rerank across axes. End with one line: findings per axis and the worst issue within each.
