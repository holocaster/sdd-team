---
name: sdd-to-tickets
description: Break a spec into tracer-bullet tickets, each declaring its blocking edges, written to the canonical local ticket directory. Deliberate fork of to-tickets for the isolated sdd-planner subagent (see .claude/skills/SYNC.md). Does not require an issue tracker.
---

# To Tickets

Break the spec into a set of **tickets**: tracer-bullet vertical slices, each declaring the tickets that **block** it.

## Process

### 1. Gather context

Read `docs/specs/<NNNN-slug>.md` (the feature id you were given) in full, plus `docs/CONTEXT.md` for vocabulary and any ADRs in the area.

### 2. Explore the codebase (optional)

If you have not already explored the codebase, do so to understand the current state of the code. Ticket titles and descriptions should use the project's domain glossary vocabulary, and respect ADRs in the area you're touching.

Look for opportunities to prefactor the code to make the implementation easier. "Make the change easy, then make the easy change."

### 3. Draft vertical slices

Break the work into **tracer bullet** tickets.

<vertical-slice-rules>

- Each slice cuts a narrow but COMPLETE path through every layer (schema, API, UI, tests): vertical, NOT a horizontal slice of one layer
- A completed slice is demoable or verifiable on its own
- Each slice is sized to fit in a single fresh context window
- Any prefactoring should be done first
- Splitting is not free: each extra ticket costs a full `sdd-implementer` + `sdd-reviewer` context reload. Only give a step its own ticket when it earns that cost - it doesn't fit one context window, or landing/reviewing it separately has real value (risk isolation, a natural checkpoint, independent demoable value). A linear chain where every ticket exists solely because the next one is blocked by it, with no standalone value, belongs in one ticket instead.

</vertical-slice-rules>

Give each ticket its **blocking edges**: the other tickets that must complete before it can start. A ticket with no blockers can start immediately.

**Wide refactors are the exception to vertical slicing.** A **wide refactor** is one mechanical change (rename a column, retype a shared symbol) whose **blast radius** fans across the whole codebase, so a single edit breaks thousands of call sites at once and no vertical slice can land green. Don't force it into a tracer bullet; sequence it as **expand–contract**. First expand: add the new form beside the old so nothing breaks. Then migrate the call sites over in batches sized by blast radius (per package, per directory), each batch its own ticket blocked by the expand, keeping CI green batch to batch because the old form still exists. Finally contract: delete the old form once no caller remains, in a ticket blocked by every migrate batch. When even the batches can't stay green alone, keep the sequence but let them share an integration branch that all block a final integrate-and-verify ticket; green is promised only there.

### 4. Self-review the breakdown

You own granularity and blocking-edge decisions - do NOT quiz the user about them. Before writing, validate your own breakdown:

- each slice is vertical and independently verifiable;
- every blocking edge is real: a ticket depends only on tickets that genuinely gate it;
- the dependency graph is acyclic and references only ticket ids that exist;
- every requirement / acceptance criterion in the spec maps to at least one ticket;
- too fine? For each ticket, name the standalone value it earns over folding it into its blocker - if you can't, merge them. A short chain of trivial, tightly-dependent tickets (a handful of acceptance criteria each, no independent demo value) is the sign to collapse it into one.

Only stop and report a pending question to your caller (`sdd-planner`) if drafting reveals a genuine **scope ambiguity or a missing/contradictory requirement** - not a granularity judgment call, which is yours to make.

### 5. Write the tickets

Canonical location: one file per ticket under `tickets/<NNNN-slug>/<NN>-<slug>.md`, numbered from `01` in dependency order (blockers first), plus `tickets/<NNNN-slug>/index.md` listing every ticket with its status and blocking edges. `index.md` is the single source of truth for status - the ticket files carry no status field. This committed directory is the authoritative ticket state. One ticket per file, never a single combined file.

If the repo has a configured issue tracker, you may additionally mirror the tickets there and record each issue id in the local file, but the local files always win.

Work the **frontier**: any ticket whose blockers are all done. For a purely linear chain that means top to bottom.

<index-template>

# Tickets: <NNNN-slug>

| # | Title | Blocked by | Status |
|---|-------|-----------|--------|
| 01 | ... | none | ready |
| 02 | ... | 01 | ready |

</index-template>

<local-ticket-template>

# <NN>: <Ticket title>

**What to build:** the end-to-end behaviour this ticket makes work, from the user's perspective, not a layer-by-layer implementation list.

**Blocked by:** the numbers/titles of the tickets that gate this one, or "None (can start immediately)".

**Spec:** `docs/specs/<NNNN-slug>.md` (section refs); **ADRs:** as relevant.

- [ ] Acceptance criterion 1
- [ ] Acceptance criterion 2

</local-ticket-template>

On the orchestrator's fast path there is no spec: write `**Spec:** none (fast path)` and make the acceptance criteria fully self-contained - they are the normative source.

In either form, name the module, area, or seam in glossary terms, and cite spec sections when there is a spec; a file or directory name is fine when it removes ambiguity. Avoid line numbers and copied code: they go stale fast. Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it and note briefly that it came from a prototype. Trim to the decision-rich parts, not a working demo, just the important bits.
