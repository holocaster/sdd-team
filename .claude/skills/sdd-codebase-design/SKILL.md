---
name: sdd-codebase-design
description: Interface and test-seam design guidance for sdd-planner. Use when the feature needs a new or changed interface, a seam choice is uncertain, or required behaviour is difficult to test through existing interfaces. Deliberate fork of codebase-design for isolated SDD planning.
---

# SDD Codebase Design

Plan deep modules: useful behaviour behind a small interface, testable through that interface. Apply this guidance only to the feature in the brief. The Planner owns the resulting spec, tickets and ADRs; this skill adds no separate design artifact or implementation phase.

Read the brief, relevant `docs/CONTEXT.md` vocabulary, `docs/adrs/` decisions, and directly relevant callers, interfaces and tests. Existing project terms and architectural constraints take precedence over this reference's design vocabulary.

## Design vocabulary

- **Module**: a function, class, package or feature slice with an interface and implementation.
- **Interface**: everything callers need to know, including inputs, outputs, invariants, ordering, errors and relevant costs.
- **Implementation**: behaviour hidden behind the interface.
- **Depth**: useful behaviour available through a small interface, not a ratio of code lines.
- **Seam**: a place where behaviour can be varied without editing its callers.
- **Adapter**: a concrete implementation satisfying an interface at a seam.
- **Leverage**: capability callers gain without learning internal details.
- **Locality**: related changes, fixes and verification concentrated in one place.

Use these terms to explain technical decisions while preserving the project's domain names. An interface can be a plain function; it does not require a language-level interface type, class hierarchy or framework.

## Choose the interface

1. Trace the behaviour required by the brief through existing callers and dependencies. Identify what the caller needs to know and what the implementation can hide. Reuse an existing interface when it already supports the required behaviour.
2. Keep the public surface small. Ask whether fewer entry points or parameters can express the same behaviour without hiding necessary invariants or errors.
3. Apply the deletion test: if removing a proposed module removes complexity, it may be unnecessary delegation; if complexity returns across callers, the module may be earning its place. Do not add pass-through layers for architectural symmetry.
4. Introduce a new seam only for concrete variation or a demonstrated testing need. Production and a justified test adapter can provide that variation; speculative future providers cannot. Internal test seams need not become public interfaces.
5. When alternatives matter, compare a few materially different interfaces within this session by caller burden, hidden complexity, locality, compatibility and testability. Choose the smallest safe option that satisfies the brief and existing decisions.

Keep dependency strategy proportional to the actual dependency:

- Pure in-process behaviour: test through the existing public interface; no adapter is needed merely to test a calculation.
- Local resources: use an available representative test stand-in when it exercises the required behaviour.
- Owned remote services: reuse an existing transport seam; propose an injected adapter only when variation or testing requires it.
- External services: isolate provider interactions at an existing seam where possible. A mock can test owned logic; provider-specific behaviour needs an appropriate integration or contract check.

## Choose the tests

Prefer the highest existing public seam that can exercise the required behaviour faithfully. Test observable results, including relevant errors and state changes. Keep the expected results independent of the implementation; avoid tests of private state or tests that restate the algorithm.

Separate pure decisions from side effects where it simplifies testing, and accept dependencies at a real seam instead of constructing them deep inside the logic. These are design choices, not requirements to rewrite existing code.

For an approved deepening/refactor, plan replacement tests at the retained interface. Retire old tests only when equivalent required behaviour is covered; do not automatically delete tests of smaller modules.

## Return to the Planner

Provide the chosen interface/seam, the concrete need it serves, relevant dependency/test strategy, and any meaningful trade-off. Incorporate the decision through `sdd-to-spec` under Implementation Decisions and Testing Decisions; subsequent tickets reference those sections. Reuse existing ADRs, and let the Planner record a new ADR only when the decision earns one.

Routine technical choices stay with the Planner. If the brief has a material gap or a high-level seam changes user-visible cost or risk, return `questions_pending` with the proposed choices for Main to resolve. Follow the Planner's existing clean-exit and handoff rules.

Do not write production code, run prototypes, spawn agents, interview the user, add requirements, or expand into a whole-codebase refactor. The upstream parallel alternative-design procedure and automatic test-deletion guidance are not part of this fork.
