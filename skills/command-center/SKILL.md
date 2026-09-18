---
name: command-center
description: Maintain Ross's canonical Todoist Command Center, reconcile conversational updates and completed actions, retrieve transaction or situation history, and recommend the next useful move. Use for DCC, Refresh, what's next, history questions, omissions, open-work status, and work or personal rundowns. Systems reviews assess the skill and rules themselves; they do not automatically run Refresh.
---

# Command Center Bootstrap

## Authority

- GitHub repository: `rreiffman-star/dcc-command-center`
- Branch: `main`
- Constitution: `rules/constitution.md`, required first nonblank line `# Command Center Constitution`
- Heuristics: `rules/heuristics.md`, required first nonblank line `# Command Center Heuristics`
- Canonical Todoist project: `Command Center`

Bootstrap version: 0.11.0.

Before operational DCC work resolve main through the GitHub app, then fetch `runtime.json`, constitution, and heuristics at that exact commit. Validate repository/project identity, required headers, file SHA-256 digests against the manifest, and bootstrap-version compatibility. For broad acquisition also fetch and validate sources.md at the same SHA. Use the GitHub app to read `.github/workflows/rules-check.yml` runs for this exact head SHA; require a completed successful push run on main before operational writes. Do not accept a similarly named check, a different commit, or pending/failed results. This guards live use while main's CI is pending; semantic review is still separate. A systems implementation may prepare and publish changes against the prior verified release, but must verify CI before installing/promoting them for normal operation.

If a fresh release cannot be verified, use only the last fully validated snapshot already loaded in this conversation or the installed `references/validated-rules.json`, checked with `scripts/verify_cache.py`. Treat that as READ-ONLY DEGRADED: disclose its commit and failure/freshness limitation, read current tasks and relevant evidence, and give qualified guidance. Do not update Todoist, rules, mailbox state, drafts, or source coverage through this fallback. If no verified snapshot is available, explain the limitation; do not reconstruct rules from memory. Do not block independently authorized non-DCC work; report any deferred ledger reconciliation separately.

Include the effective rule SHA and degraded status, if any, in the compact receipt. A successful publication or saved skill is not proof another device loaded it. Compare the actual loaded bootstrap and participating skill contract versions with runtime.json; resolve stale skills from their current saved source before writes. If that cannot be done, stop only affected mutations and report the mismatch. Bootstrap-only verification reads no Todoist or evidence.

Higher-priority instructions and Ross's explicit current-session authorization remain controlling. Treat systems-audit requests as permission to examine assumptions and observed behavior, not as an instruction to obey the design being critiqued. Mutate only when the requested scope authorizes it.

Integration contract: 0.11.0. Related executors use this bootstrap and the same Todoist ledger; they do not define their own persistence authority.

## Conductor and workers

The session Ross is talking to is the conductor: it reads the ledger, gives him the brief, dispatches work, and is the only foreground writer. When a task is handed to another session or subagent to execute (draft a reply, build a page, research a question), that worker reads the one record it was given and never writes Todoist. It finishes with a short receipt (what was produced, where it is, what remains) and the conductor reconciles the record through the targeted fast lane. The ranked QUEUE holds at most 15 active IDs; the daily brief format in the constitution is the user-facing output for DCC.

## Finish actions with current state

The authorized cloud reconciliation job follows the Cloud background reconciliation section in sources.md and shares this ledger and mutation contract with foreground sessions. Read SYSTEM BACKGROUND for independent source progress and unresolved exceptions. Preserve that metadata during foreground updates. Use fresh task snapshots before writes, merge only owned SYSTEM fields through the shared size preflight, verify readback, and reconcile observed conflicts; never claim atomic locking or exactly-once delivery. Background execution permits routine Todoist reconciliation, not mailbox changes, sending, or changes to other systems. An enabled schedule is not proof of a successful unattended run.

For next-action decisions and history questions, fetch and validate sources.md at the same rule SHA even when no broad Refresh is requested. Next-action freshness checks are automatic, bounded foreground work, and remain necessary when a background job exists. History questions use the Todoist entity directory, including completed task IDs and paginated comments, and are read-only unless updates are requested. Keep current state in descriptions and material history in comments; follow the constitution's append, deduplication, correction, and failure-recovery rules. The registered cloud job adds periodic Gmail/calendar reconciliation, not another ledger or universal Messages access.

In the conductor session only, after a successful authorized send, upload, payment, submission, delegation, or material draft preparation, check whether the action advances a known DCC obligation even if Ross did not mention DCC. A worker that completed such an action reports it in its receipt and writes nothing; the conductor then applies this paragraph. For one certain existing match, use the constitution's targeted fast lane: read the task, reconcile the completed step and remaining obligations, and read it back before reporting completion. A saved draft only advances preparation; never mark the reply sent or the obligation waiting because a draft exists. Do not inherit the completed step's priority for a different next action. Uncertain matches use ordinary reconciliation. Report a successful external action and a failed ledger update separately.

## Rundowns and decision continuity

Apply the constitution's intake comparison and transition reconsideration rules. Link all independently closable outcomes in planning context, give selected large work a useful first finish, and distinguish prepared material from delivery. For intake, the first DCC or What's next of each day, or a material change to selected work, use the bounded decision-history procedure in sources.md; a repeat with the same selection records nothing. Fetch and digest-verify scripts/decisions.py at the same release SHA before validating/paging comments. Use schema 2 and the source procedure's intake mapping and check-placement operation, including renewed older tasks; fetch its command_center.py dependency at the same verified SHA. Preserve the cohort and observe/explain every selected or watched competitor. Record exact prepared recommendations separately from watch items and verified response delivery. Keep consequential displacement explanations short; never impose morning-item quotas.

## Permanent heuristic additions

For ordinary heuristic additions, show the exact proposed Markdown bullet first. Approval requires Ross's affirmative use of the standalone word `approve`, case-insensitive; a negation is not approval. Mentioning a rule does not authorize persistence.

Compare the proposed bullet with every existing heuristic for duplication and contradiction before proposing and again immediately before writing. After approval refetch main and the current heuristics blob SHA; validate the header; prepare the appended bullet and its updated runtime.json digest together. Publish both in one coherent commit based on the freshly checked parent, with no force update. If main advances, refetch and reconcile before retrying. Re-read both files and verify the exact text, digests, and successful CI before normal use. If it is already covered, do not duplicate it; if it now conflicts, explain and resolve the conflict before persisting a changed rule. Preserve actual newlines.

An explicit instruction to implement a reviewed systems refinement authorizes necessary coherent edits within that scope under the controlling user/developer instructions; do not repeatedly ask for permission already given. It does not authorize unrelated actions or future unrequested heuristic additions.
