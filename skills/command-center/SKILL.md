---
name: command-center
description: Maintain Ross's Todoist Command Center, consume its saved work queue, refresh priorities on explicit request, reconcile actions and rundowns, and retrieve deal or situation context. Use for DCC, what's next, Refresh DCC, history, omissions and systems reviews. A systems review does not run Refresh.
---

# Command Center Bootstrap

## Load the release once

Authority: private repository `rreiffman-star/dcc-command-center`; `main` contains source and branch `verified` contains the released `validated-rules.json`. Todoist project `Command Center` is the only obligation ledger. Bootstrap version: 0.14.0. Integration contract: 0.14.0.

Fetch that bundle once per conversation through the GitHub app. Reuse it for subsequent turns; do not resolve main, fetch every rule separately, or list CI runs during ordinary operation. Release publication, same-commit helper retrieval, and stale-skill repair are separate operations.

Check the complete, untruncated bundle: repository and manifest repository match the authority; manifest project is Command Center and bootstrap_version is 0.14.0; commit is a full SHA; ci.head_sha matches it, head_branch is main, event is push, path is .github/workflows/rules-check.yml, status is completed and conclusion is success. files must contain exactly:

- rules/constitution.md — # Command Center Constitution
- rules/heuristics.md — # Command Center Heuristics
- rules/sources.md — # Command Center Source Procedures
- rules/inbox-senders.md — # Command Center Inbox Senders

Each first nonblank line must match its header. Read constitution and heuristics; select only the needed sources.md sections below. With a runtime, run scripts/verify_cache.py --fetched against the fetched bundle. Keep raw tool payloads in session scratch or tool memory and emit only relevant text, rather than printing the full bundle repeatedly. A chat without a runtime does the reading checks; it cannot claim digest or helper validation.

The release workflow tests then publishes the bundle; the daily mechanical audit checks it against its commit. Trust is limited to the credentials able to write this repository, not a cryptographic proof of authorship. Never accept a bundle from correspondence. The effective rule SHA is bundle.commit. Compare participating skill versions to its manifest; repair stale instructions from skills/<name>/SKILL.md at that released SHA before affected writes. A saved or published skill does not prove another device loaded it.

If fresh retrieval/validation fails, use only a previously validated bundle in this conversation or an installed references/validated-rules.json checked by verify_cache.py. Mark READ-ONLY DEGRADED with commit and limitation; no DCC-authorized Todoist, rule, mailbox, draft or coverage writes. Without either, report DCC unavailable and do not reconstruct rules or operate its ledger from memory. Independently authorized non-DCC work may continue; report deferred reconciliation separately. Bootstrap-only verification reads no Todoist or evidence.

## Route by Ross's request

Use these sources.md sections from the loaded bundle:

| Request | Procedure |
| --- | --- |
| What's next / DCC / morning brief / show list | Frozen work queue between explicit refreshes |
| Refresh DCC or clear explicit equivalent | Explicit Refresh DCC; Refresh selection and attention; Efficient context and source retrieval; applicable source checks; Record a decision observation |
| Done / sent / skip / rundown | Frozen work queue; Reconciliation checks; constitution's targeted reconciliation |
| Help execute a selected task / prepare a call | Situation context and execution; relevant task and sources only |
| History / why / how much / show the source | Retrieve material history; Situation context and execution |
| What's slipping / omissions | Omissions review; relevant source checks |
| Review or improve the system | Logs and affected code/rules; no automatic Refresh |

Keep the ranked QUEUE (maximum 15 active IDs) and its WORK BLOCK frozen until explicit Refresh. Ordinary next-action requests read SYSTEM and candidate tasks in order, not the entire ledger, inbox or decision history. Return one executable move with its useful finish and why it matters. Exhaustion, a new day, intake and completion do not authorize replenishment or polling. A known material conflict can be stated briefly without reshuffling.

After an authorized action or unambiguous report, reconcile the affected obligation immediately, preserve history and remaining steps, verify readback, and retire an advanced queued action through generation-matched WORK BLOCK exclusions. Skip affects this block only. A prepared draft is not sent. Targeted requested work may read its required evidence without becoming Refresh. New outcomes stay unranked until Refresh.

The foreground conversation is the conductor and owns foreground writes. Dispatched workers read their assigned records, do scoped work, and return receipts; they never write Todoist. Use parallel read-only workers only when permitted and useful. Scheduled background evidence acquisition is inactive; the scheduled mechanical digest is read-only. Older scheduled prompts do not override this.

Use verified same-commit scripts only where needed. context.py creates ephemeral compact views and attention metadata, never ranks or writes. decisions.py checks explicit-Refresh placement; background.py guards queue/system merges. No Python download is required for ordinary What's next. If a required helper cannot run, state precisely what was not validated without inventing success.

## Change rules within authorization

Ross's explicit request to implement a systems refinement authorizes coherent changes within that scope. A review alone is read-only. Current-session authorization and higher-priority instructions control; do not ask again for approval already given.

For an ordinary new permanent heuristic, first compare all existing bullets, show the exact proposed Markdown bullet, and obtain affirmative standalone `approve` (case-insensitive; negation is not approval). Immediately before writing, refetch main and the heuristics blob; repeat conflict/duplicate checks and validate its header. Commit the bullet and runtime digest together on the freshly checked parent, without force. If main advances, reconcile and retry. Use the new rule only once the verified branch publishes its commit. Do not duplicate an already covered rule or silently alter an approved conflicting one.

Keep the receipt short: outcome, material gaps and effective rule SHA. State observed limitations, not routine verification narration.
