---
name: sdd-implement
description: Implement one ticket, or each ticket in a Batch, based on its spec references. Deliberate fork of implement for the sdd-implementer subagent (see .claude/skills/SYNC.md). Self-review only - independent review is a separate sdd-reviewer pass.
---

Implement the behavior described by the ticket (or, for a Batch, each ticket in order) and its spec references.

Invoke the "tdd" skill with the glossary path `docs/CONTEXT.md` and ADR directory `docs/adrs/`; these SDD paths override its default `GLOSSARY.md` and `docs/adr/` paths, including in referenced guidance. Work test-first where possible, at pre-agreed seams.

Run typechecking regularly, single test files regularly, and the full test suite once at the end.

On a correction round, when a finding is about a *class* of defect - an unguarded overflow, an unhandled input shape, a missing boundary check, a leaked stream - fix every sibling occurrence of that class in the same function or module in this round, not only the exact line the reviewer cited. Grep the surrounding code for the pattern before you commit. Siblings of a cited finding are in scope; leaving them for the next round is what turns one correction into three.

Do a quick self-check of your own diff for obvious slop (dead code, reinvented stdlib, unrequested abstraction), then commit to the current branch. Do NOT run a full `code-review` - that is `sdd-reviewer`'s independent pass, and running it here just duplicates it.

Report the commit sha of your final commit as `head_sha`.
