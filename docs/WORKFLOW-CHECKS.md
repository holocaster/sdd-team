# Workflow acceptance scenarios

These scenarios check the contracts in [sdd-main](../.claude/skills/sdd-main/SKILL.md),
[Reviewer](../.claude/agents/sdd-reviewer.md), and
[Implementer](../.claude/agents/sdd-implementer.md). They are manual acceptance cases,
not an executable workflow engine or proof that a model follows the instructions.
Use disposable Git repositories for destructive or interrupted-run fixtures.

The [automated script checks](../tests/test_scripts.py) cover bootstrap and profile
synchronization; run them with the command in [README](../README.md#desenvolvimento-e-referências).
They do not evaluate agents against the manual scenarios below.

## Dispatch and review readiness

Evaluate Main's next action with the stated authorization, harness capabilities,
Git state and agent result. Use tool-call traces to check dispatch timing and
context inheritance; a promise to use an isolated agent is not sufficient.

| Initial condition | Expected result |
|---|---|
| Required commits lack user authorization | Ask only for missing authorization; no dependent dispatch or unauthorized commit. |
| User already authorized the required local commits | Reuse that authorization; no repeated permission question. |
| Worktree is writable but harness denies Git metadata writes, or the required checkpoint fails | Report the environment blocker before dispatch; preserve work; wait for the environment to change. |
| Harness offers parent-conversation inheritance | Disable inheritance for every role, including correction and retry spawns; in Codex use `fork_turns: "none"`. |
| Dispatch to Planner, Implementer or Reviewer | New isolated session with objective, references and necessary constraints; correction also carries immutable base and findings; no copied chat, documents or prior reasoning. |
| Harness cannot create a fresh isolated session | Report missing capability; no substituted inline role. |
| Implementer is still running or has returned a blocked result | Wait or route the blocker; no Reviewer dispatch. |
| Handoff claims `ready_for_review` but a SHA is missing/unresolvable, base equals head, or commits are not in ancestry order on the current branch | No Reviewer dispatch; complete the handoff when prerequisites allow, or resolve uncertain history with the user. |
| Implementation is only staged or unstaged, with no final commit | Preserve work; no snapshot/empty-range substitute for review; resolve the commit blocker first. |
| Completed ticket/Batch has valid distinct SHAs and clean tree, with only later Main bookkeeping commits | Review the exact implementation range; keep implementation unchanged until Reviewer returns. |
| Cold resume finds verified implementation commits but the handoff was lost | Recover pointers under Phase 6; apply the same commit/tree checks; review without requiring a replacement handoff. |

## Local work

Record file bytes, index contents, and Git status before each case. Compare them
afterward; preserving a path while changing its contents is a failure.

| Initial condition | Expected result |
|---|---|
| Cold resume with an unstaged tracked edit | Preserve it; report paths to the user; no state write or agent spawn. |
| Cold resume with staged changes and a different working-tree version | Preserve both versions and the index; report paths; no state write or spawn. |
| Cold resume with untracked user notes | Preserve the notes; report paths; no state write or spawn. |
| Reviewer enters with a dirty tree | Preserve all changes; return `blocked` before checks. |
| Implementer enters with a dirty tree | Preserve all changes; return `blocked_technical` before implementation. |
| Check modifies a known tracked fixture and creates a new temporary file | Restore only that fixture to its entry contents and remove only the created file. |
| Check changes the index or leaves a file whose ownership is uncertain | Preserve that work; Reviewer returns `blocked` with remaining paths; Main waits for the user. |
| Implementer stops blocked with its own known unstaged edits and temporary files | Clean only its own paths; no global cleanup. |
| Implementer stops blocked with staged or uncertain changes | Preserve them and report paths; Main resolves the dirty tree before another spawn. |

## Cold resume

Use one ticket `01` with pending criteria and these commits on a linear branch:

- `C`: Main activates the ticket; both SHAs and `review` are null; `review_round: 0`.
- `I`: Implementer commits the implementation, starting from `C`.
- `S`: Main saves `base_sha: C`, `head_sha: I`.
- `R`: Main saves a review for ticket `01` over `C..I` and its resulting counter.
- `F`: Implementer commits a correction after `R`, retaining base `C`.
- `S2`: Main saves `head_sha: F`, clears `review`, and retains base and counter.

Each row starts from the committed state at the named tip, with a clean tree.
Evaluate the ordered cold-resume steps against the commit contents and state.

| Branch tip and state | Expected route and invariant |
|---|---|
| `C`, no implementation | Spawn first-round Implementer. |
| `I`, SHAs not saved | Recover `C..I`, commit pointers, then review that exact range. |
| `S`, no review | Review `C..I`; do not replace `I` with `S`. |
| `R`, `changes_requested`, round 1 | Correction with base `C` and saved findings; counter remains 1; no repeated review. |
| `R`, `changes_requested`, round 3 | Escalate to user; no agent spawn or counter increment. |
| `R`, `blocked` | Relay verification blocker to user; no Implementer spawn. |
| `R`, a finding needs a product decision | Relay decision to user. |
| `R`, `approved`, approval commit pending | Mark ticket done and criteria checked; clear active pointers and counter. |
| `F`, saved head still `I`, old review `C..I` | Recover `C..F`, clear review pointer, retain counter; review before any further correction. |
| `S2`, no review | Review `C..F`; preserve original base and counter. |
| Later commit only persists Main state | Keep saved implementation head and reuse a matching review. |
| Later Implementer commits introduce and then revert a change | Recover the last Implementer commit; an empty net diff does not make those commits bookkeeping. |
| Saved review names another ticket or range | Review the active range; do not route the mismatched review. |
| Missing SHAs, rewritten history, or unknown commit ownership | Preserve pointers; ask user rather than infer a new base or head. |

Repeat with `active_ticket: [01, 02]` and a Batch review: correction and approval
apply to both tickets; the original base and one review counter remain shared.

## Review scope

For each case, assume all active criteria pass and required checks are complete.

| Evidence | Expected result |
|---|---|
| Parser accepts a new format but breaks an old supported format; base/head comparison proves the regression | `blocking`, `changes_requested`, even without an old-format criterion. |
| The same defect exists at base and head and is outside the active criteria | Report as pre-existing; it alone does not change `approved`; Main routes separately. |
| A future format belongs to another ticket and was never supported | Out of scope; it alone does not change `approved`. |
| Old behavior changes intentionally as required by the approved spec | Judge against that requirement; the intended change alone is not a regression. |
| Regression is only suspected, without reproduction or deterministic source proof | Record uncertainty in `residual_risks`; do not claim a proven regression. |
| One Batch member introduces a proven regression outside its literal criteria | Entire Batch is `changes_requested`; neither member is marked done. |

## Spec synthesis

Evaluate [sdd-to-spec](../.claude/skills/sdd-to-spec/SKILL.md) in separate fresh
sessions for the two briefs below. Use temporary directories, write only the spec,
and make no commits. Give each agent its brief, feature id, skill and this fixture
context; keep the expected results for the evaluator.

Fixture context: a local task list is an ordered Python list of dictionaries with
`id`, `title` and `completed`. Existing `list_tasks(tasks)` returns a shallow copy
of each dictionary in order. There is no persistence, networking or authentication;
tests exercise public functions. There are no open product questions.

### Small brief: `0001-export`

Add `export_task_ids(tasks)` returning a JSON array string of task ids in their
existing order. An empty list produces `[]`; input tasks remain unchanged. The
agreed public serialization contract uses JSON numbers for integer ids, including
ids above 2^53. Consumers must decode those integers without loss; browser-number
interoperability is outside scope. Exclude files, CLI commands, filtering,
metadata, persistence, authentication, other formats and changes to `list_tasks`.

### Larger brief: `0002-manage`

- `add_task(tasks, title)` appends an incomplete task with a trimmed title and a
  positive id above all current ids (1 when empty). Blank titles raise `ValueError`.
- `rename_task(tasks, task_id, title)` changes only the trimmed title; blank titles
  raise `ValueError`.
- `set_completed(tasks, task_id, completed)` sets only the flag; repeating a value
  is valid.
- `delete_task(tasks, task_id)` removes only that task, preserving remaining order.
- These three id-based operations raise `KeyError` for an unknown id, before title
  validation. Every rejected operation leaves the list unchanged.
- `list_tasks(tasks, completed=None)` returns dictionary copies in existing order:
  `None` includes all tasks, `True` or `False` filters by the flag. Editing returned
  dictionaries leaves stored tasks unchanged.
- `summarize_tasks(tasks)` returns `total`, `completed` and `pending` counts, all
  zero when empty. Mutations operate in place and return `None`. Inputs have their
  declared types; existing ids are unique positive integers. Exclude type coercion,
  extra validation, persistence, CLI/UI, users, authentication, networking, sorting,
  bulk operations, due dates, labels, export and undo.

### Expected results

Every agreed behavior and constraint appears in the spec, every story traces to
the brief, and each story contributes a distinct outcome or acceptance condition.
The small case retains its serialization decision without unrelated features;
the larger case retains error precedence, unchanged-on-error behavior, copy
isolation and mutation contracts. Judge coverage and relevance, not story count
or document length. Record missing or invented requirements per case. This checks
spec synthesis only, not the complete Planner or implement/review workflow.
