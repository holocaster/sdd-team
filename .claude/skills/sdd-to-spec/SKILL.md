---
name: sdd-to-spec
description: "Synthesize a feature brief into a spec and write it to the canonical local path. No interview - just synthesis. Deliberate fork of to-spec for the isolated sdd-planner subagent (see .claude/skills/SYNC.md). Does not require an issue tracker."
---

This skill takes the feature brief (`docs/briefs/<NNNN-slug>.md`), the conversation context, and codebase understanding and produces a spec. Do NOT interview the user; just synthesize what you already know.

## Process

1. Explore the repo to understand the current state of the codebase, if you haven't already. Use `docs/CONTEXT.md` glossary vocabulary throughout the spec, and respect any ADRs in the area you're touching.

2. Sketch out the seams at which you're going to test the feature. Existing seams should be preferred to new ones. Use the highest seam possible. If new seams are needed, propose them at the highest point you can. The fewer seams across the codebase, the better - the ideal number is one.

   Do NOT ask the user. Record the chosen seams in "Testing Decisions". If a seam choice is genuinely ambiguous or forces a new high-level seam that changes user-visible cost or risk, do not decide it silently - stop and report it to your caller (`sdd-planner`) as a pending question.

3. Write the spec using the template below to `docs/specs/<NNNN-slug>.md`, using the feature id you were given. This committed file is canonical. If the repo has a configured issue tracker, you may additionally publish there and note the issue id in the spec, but the file always wins.

<spec-template>

## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## User Stories

A numbered list of distinct user stories, proportional to the agreed feature scope. Each user story should be in the format of:

1. As an <actor>, I want a <feature>, so that <benefit>

<user-story-example>
1. As a mobile bank customer, I want to see balance on my accounts, so that I can make better informed decisions about my spending
</user-story-example>

Cover every behavior and constraint agreed in the brief, using only stories that add a distinct user outcome or acceptance condition. Merge duplicates and keep each story traceable to the brief; do not invent requirements to lengthen the list.

## Implementation Decisions

A list of implementation decisions that were made. This can include:

- The modules that will be built/modified
- The interfaces of those modules that will be modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

Do NOT include line numbers or copied code, and prefer module/area names in glossary terms over full file paths. They go stale quickly.

Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it within the relevant decision and note briefly that it came from a prototype. Trim to the decision-rich parts, not a working demo, just the important bits.

## Testing Decisions

A list of testing decisions that were made. Include:

- A description of what makes a good test (only test external behavior, not implementation details)
- Which modules will be tested
- Prior art for the tests (i.e. similar types of tests in the codebase)

## Out of Scope

A description of the things that are out of scope for this spec.

## Further Notes

Any further notes about the feature.

</spec-template>
