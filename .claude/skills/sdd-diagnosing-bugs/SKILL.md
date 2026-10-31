---
name: sdd-diagnosing-bugs
description: Read-only diagnosis of suspected bugs and performance regressions during SDD review. Use when sdd-reviewer needs to reproduce a defect, investigate its cause, or verify a correction. Deliberate fork of diagnosing-bugs; returns evidence through the existing reviewer handoff.
---

# SDD Diagnosing Bugs

Diagnose the suspected defect and return evidence to `sdd-reviewer`. The Implementer owns fixes, instrumentation changes, and permanent regression tests.

## Scope and inputs

Use the caller's ticket or Batch, normative spec/acceptance criteria, suspected symptom, and exact `base_sha..head_sha` range. Read `docs/CONTEXT.md` for vocabulary and relevant `docs/adrs/` for decisions. Trace relevant callers and dependencies without expanding the review into unrelated work.

Run checks against the implementation at `head_sha`. `HEAD` may include later bookkeeping commits; establish that the code exercised matches `head_sha` before attributing a result to the reviewed range. Compare with `base_sha` when needed to distinguish an introduced regression from a pre-existing defect.

Keep repository code, tests, requirements, and Git state unchanged. Use existing checks, direct invocations, or temporary probes and fixtures outside the repository. Probes must exercise the actual implementation, not a rewritten copy of the suspected logic. Use available tools and dependencies. Do not add logs, patch code, switch commits, spawn agents, or contact the user.

Redact secrets from commands, outputs, and captured artifacts. If access, information, or permission is missing, report it to the Reviewer for Main to resolve.

## 1. Build a feedback loop

Prefer a failing test at the relevant public seam, a CLI invocation, a local HTTP/browser check, or replay of an available trace. For intermittent failures, use a seeded property/fuzz probe or a differential check when appropriate. Keep the loop fast, symptom-specific, and reproducible; for flaky failures, record the conditions and observed failure rate.

This phase is complete when you have executed one command that exercises the actual suspected path and detects the expected failure. Record the command, expected behaviour and its normative source, actual output, and code snapshot tested. A command that merely runs without crashing is insufficient when the symptom is incorrect output.

If execution is unavailable or the symptom cannot be reproduced, record what you tried and the limitation. A deterministic source-level proof can support a finding; distinguish it from a runtime reproduction. An untested hypothesis is a residual risk, not a proven defect. Missing required behaviour can be established from the source without inventing a failing runtime test.

## 2. Reproduce and minimise

Confirm the loop detects the suspected symptom rather than a nearby failure. Reduce inputs, fixtures, and steps one at a time, rerunning after each reduction. Preserve the original scenario for the handoff.

Stop minimising when every remaining element is needed to trigger the same failure. Keep the expected result independent of the implementation under review.

## 3. Form and test hypotheses

For a non-obvious cause, list several ranked, falsifiable hypotheses before testing them. State the prediction each makes. When the evidence directly proves the cause, explain it instead of generating unnecessary alternatives.

Test one prediction at a time through controlled inputs, existing logs, read-only debugger/REPL inspection, or temporary probes. For performance regressions, measure the relevant scenario and compare equivalent conditions before calling it a regression. Code instrumentation and fixes belong to the Implementer.

Record which predictions held or failed. Keep confirmed causes separate from likely causes. A proven symptom is still a valid finding when its root cause remains uncertain; do not prescribe a speculative patch.

## 4. Return evidence for review

Use the Reviewer's existing handoff fields:

- `findings`: include the location, violated criterion or invariant, impact, minimal reproduction command/input, expected versus actual result, and cause evidence. State whether the defect is introduced or pre-existing, or whether attribution remains uncertain. Describe the required behaviour; the Implementer chooses the fix.
- `checks`: record the command, `passed` / `failed` / `not_run`, and evidence. A reproduction that exposes a defect is a failed check, even though the diagnosis succeeded. Include original-scenario verification when checking a correction.
- `residual_risks`: list unverified hypotheses, missing access, and checks that could not run. Return `blocked` when a required reference or unavailable environment prevents completing the review, rather than asserting approval or a defect without evidence.

The Reviewer's existing verdict and scope rules remain authoritative: confirmed in-scope blocking/important defects require correction; an out-of-scope defect is reported for Main to route and does not change the active ticket's verdict. Passing a minimal probe alone does not establish that every acceptance criterion is met.

Remove temporary artifacts you created and follow the Reviewer's clean-exit procedure if a check generated repository files. Return the evidence without committing or fixing anything.
