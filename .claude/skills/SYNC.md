# Skill forks

`sdd-grill-with-docs`, `sdd-to-spec`, `sdd-to-tickets`, `sdd-implement`, `sdd-code-review`
started as copies of the corresponding [Matt Pocock skills](https://github.com/mattpocock/skills)
with `disable-model-invocation: true` removed so the SDD subagents can invoke them.

`sdd-diagnosing-bugs` is a read-only fork of `diagnosing-bugs`, based on upstream
[`d81f3a183412e71a5b1e84ca21bc1a35eea03a60`](https://github.com/mattpocock/skills/blob/d81f3a183412e71a5b1e84ca21bc1a35eea03a60/skills/engineering/diagnosing-bugs/SKILL.md).

`sdd-codebase-design` forks `codebase-design` and selected dependency/test guidance from
`DEEPENING.md`, based on the same upstream
[`d81f3a183412e71a5b1e84ca21bc1a35eea03a60`](https://github.com/mattpocock/skills/tree/d81f3a183412e71a5b1e84ca21bc1a35eea03a60/skills/engineering/codebase-design).

They are **deliberate forks, not transparent wrappers.** They diverge on purpose:

- `sdd-to-spec` / `sdd-to-tickets`: the "check with the user" / "quiz the user, iterate until
  approval" steps are removed. An isolated subagent cannot talk to the user. The planner owns
  granularity and blocking-edge decisions and only stops (`questions_pending`) on genuine
  scope/product gaps.
- `sdd-to-spec`: user stories cover the agreed brief with proportional detail, distinct
  outcomes and traceable requirements, replacing upstream's demand for a long, extensive list.
- `sdd-to-tickets` specifically: removing "quiz the user" also removed upstream's only check
  against over-splitting (the user asking "too fine?"). Replaced with an explicit self-check -
  splitting costs a full implementer + reviewer context reload per ticket, so a step only earns
  its own ticket when it doesn't fit one context window or has real standalone value.
  `sdd-main` Phase 3 can Batch several
  already-frontier tickets into one implementer spawn and one reviewer spawn over their
  combined range - one review record, one `review_round` counter, corrected and approved as
  a unit. This saves context reloads without forcing the planner to under-split.
- Canonical artifact locations are fixed to committed local files: `docs/specs/<NNNN-slug>.md`,
  `tickets/<NNNN-slug>/` with an `index.md`. Not `.scratch/`, not "the tracker". A tracker is
  an optional mirror.
- No dependency on `/setup-matt-pocock-skills`.
- `sdd-grill-with-docs` / `sdd-implement`: invoke upstream `domain-modeling` / `tdd`
  with SDD path overrides: glossary in `docs/CONTEXT.md`, ADRs in `docs/adrs/`.
  These overrides also apply to upstream format references, which now name `GLOSSARY.md`
  and `docs/adr/`. Discovery preserves the other sections of `CONTEXT.md` and passes
  ADR proposals to the planner, which owns writing ADRs. The upstream dependencies
  are used directly, without SDD-specific edits.
- `sdd-implement`: the trailing `code-review` call is removed - independent review is a
  separate `sdd-reviewer` pass. Reports `head_sha`. Adds a correction-round rule: fix every
  sibling of a cited finding in the same function/module in that round.
- `sdd-code-review`: targets an explicit `base_sha..head_sha` range instead of `HEAD` (so
  the orchestrator's later checkpoint commits do not drift the endpoint); the
  `docs/agents/issue-tracker.md` gate is removed; the two axes run in sequence rather than as
  parallel sub-agents, because a subagent cannot spawn its own sub-agents. It consumes sanitized
  context from the Reviewer's preceding BRANCH security pass. Bookkeeping paths
  (`.ai/**`, `tickets/**` non-code) are excluded from application review, but not credential scanning.
- `sdd-diagnosing-bugs`: keeps reproduction, minimisation and hypothesis testing, but
  replaces instrumentation/fix/test-writing phases with read-only probes and an evidence
  handoff to the Reviewer. User questions go through Main; paths follow SDD conventions.
  Findings use the existing review schema and exact range. Runtime reproduction is preferred;
  source-level proof remains valid, and untested hypotheses stay residual risks. No HITL
  script is copied because the Reviewer cannot contact the user.
- `sdd-codebase-design`: conditionally guides Planner interface and test-seam choices before
  spec synthesis. Uses SDD paths and existing domain vocabulary, compares alternatives in
  the same session, and returns product/cost/risk questions through Main. It adds no code,
  prototypes, nested agents or separate design artifacts. Test retirement requires equivalent
  coverage rather than upstream's blanket deletion of old shallow-module tests.

`sdd-main` and `sdd-security-review` are separate workflow skills, outside this fork inventory.

## Re-syncing from upstream

There is no automatic sync. When the upstream skills change materially, diff them against
these forks by hand and decide what to carry over. Because the forks change workflow
semantics (approval ownership, artifact paths), a blind re-copy would break the SDD flow -
review every hunk. The upstream commit these were forked from is recorded in git history of
this file's first commit.
