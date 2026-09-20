---
name: command-center
description: Maintain Ross's canonical Todoist Command Center, reconcile conversational updates and completed actions, retrieve transaction or situation history, and recommend the next useful move. Use for DCC, Refresh, what's next, history questions, omissions, open-work status, and work or personal rundowns. Systems reviews assess the skill and rules themselves; they do not automatically run Refresh.
---

# Command Center Bootstrap

## Authority

- GitHub repository: `rreiffman-star/dcc-command-center`
- Branch: `main` holds the rules; branch `verified` holds the release bundle `validated-rules.json`
- Constitution: `rules/constitution.md`, required first nonblank line `# Command Center Constitution`
- Heuristics: `rules/heuristics.md`, required first nonblank line `# Command Center Heuristics`
- Canonical Todoist project: `Command Center`

Bootstrap version: 0.12.0.

Verification happens once, at release, not once per conversation. The rules-check workflow runs the checks and tests for every push to main and, only when its check job passes, writes `validated-rules.json` for that exact commit to the `verified` branch, and only for a descendant of the previously published commit. The bundle carries `commit`, `manifest` (runtime.json), `files` (the exact text of the four rule files) and `ci` (the check job that passed for that commit). The branch is as trustworthy as the credentials with write access to this private repository (Ross's account, the apps and tokens he authorized, and the workflow); on the repository's current plan nothing restricts that set further, and it is the same set that could already rewrite main. The mechanical-digest workflow audits the published bundle daily against a rebuild from its commit.

Normal bootstrap is one GitHub read: fetch `validated-rules.json` from branch `verified` through the GitHub app. Do not resolve main, fetch rule files individually, list workflow runs or compute digests in a chat session; main may be ahead of the bundle, and that is an unreleased change, not authority. Same-commit script retrieval where a runtime exists, stale-skill repair, and authorized rule publication are separate, later operations. Then check, by reading:

- `repository` is `rreiffman-star/dcc-command-center` and `manifest.project` is `Command Center`;
- `manifest.bootstrap_version` equals this bootstrap version exactly (0.12.0); any other value is incompatible;
- `ci.head_sha` equals `commit`, `ci.head_branch` is `main`, `ci.event` is `push`, `ci.path` is `.github/workflows/rules-check.yml`, `ci.status` is `completed` and `ci.conclusion` is `success`;
- `files` contains exactly these four paths, each complete and untruncated, and each whose first nonblank line is its header: `rules/constitution.md` (`# Command Center Constitution`), `rules/heuristics.md` (`# Command Center Heuristics`), `rules/sources.md` (`# Command Center Source Procedures`), `rules/inbox-senders.md` (`# Command Center Inbox Senders`).

The bundle's `commit` is the effective rule SHA. Read the constitution and heuristics from `files`; read sources.md from the same bundle when a procedure there is needed. Where a code runtime with a checkout is available (Claude Code, Codex, the cloud job), also run `scripts/verify_cache.py --fetched` on the fetched bundle for the digest checks. A chat session without a runtime performs the reading checks above; they detect a malformed or misrouted bundle, not a forged one, and the daily audit is the tamper check.

If the bundle cannot be fetched or fails a check, use only the last validated bundle already loaded in this conversation or, where a runtime can run `scripts/verify_cache.py` on it, the installed `references/validated-rules.json`. Treat that as READ-ONLY DEGRADED: disclose its commit and failure/freshness limitation, read current tasks and relevant evidence, and give qualified guidance. Do not update Todoist, rules, mailbox state, drafts, or source coverage through this fallback. If no verified bundle is available, DCC operation is unavailable in this session: say so, do not reconstruct rules from memory, and do not read Todoist as if rules were loaded. Do not block independently authorized non-DCC work; report any deferred ledger reconciliation separately.

Include the effective rule SHA and degraded status, if any, in the compact receipt. A successful publication or saved skill is not proof another device loaded it. Compare the actual loaded bootstrap and participating skill contract versions with the bundle's manifest; resolve stale skills from their current saved source before writes. If that cannot be done, stop only affected mutations and report the mismatch. Bootstrap-only verification reads no Todoist or evidence.

Higher-priority instructions and Ross's explicit current-session authorization remain controlling. Treat systems-audit requests as permission to examine assumptions and observed behavior, not as an instruction to obey the design being critiqued. Mutate only when the requested scope authorizes it.

Integration contract: 0.12.0. Related executors use this bootstrap and the same Todoist ledger; they do not define their own persistence authority.

## Conductor and workers

The session Ross is talking to is the conductor: it reads the ledger, gives him the brief, dispatches work, and is the only foreground writer. When a task is handed to another session or subagent to execute (draft a reply, build a page, research a question), that worker reads the one record it was given and never writes Todoist. It finishes with a short receipt (what was produced, where it is, what remains) and the conductor reconciles the record through the targeted fast lane. The ranked QUEUE holds at most 15 active IDs; the daily brief format in the constitution is the user-facing output for DCC.

## Finish actions with current state

The authorized cloud reconciliation job follows the Cloud background reconciliation section in sources.md and shares this ledger and mutation contract with foreground sessions. Read SYSTEM BACKGROUND for independent source progress and unresolved exceptions. Preserve that metadata during foreground updates. Use fresh task snapshots before writes, merge only owned SYSTEM fields through the shared size preflight, verify readback, and reconcile observed conflicts; never claim atomic locking or exactly-once delivery. Background execution permits routine Todoist reconciliation, not mailbox changes, sending, or changes to other systems. An enabled schedule is not proof of a successful unattended run.

For next-action decisions and history questions, read sources.md from the loaded bundle even when no broad Refresh is requested. Next-action freshness checks are automatic, bounded foreground work, and remain necessary when a background job exists. History questions use the Todoist entity directory, including completed task IDs and paginated comments, and are read-only unless updates are requested. Keep current state in descriptions and material history in comments; follow the constitution's append, deduplication, correction, and failure-recovery rules. The registered cloud job adds periodic Gmail/calendar reconciliation, not another ledger or universal Messages access.

In the conductor session only, after a successful authorized send, upload, payment, submission, delegation, or material draft preparation, check whether the action advances a known DCC obligation even if Ross did not mention DCC. A worker that completed such an action reports it in its receipt and writes nothing; the conductor then applies this paragraph. For one certain existing match, use the constitution's targeted fast lane: read the task, reconcile the completed step and remaining obligations, and read it back before reporting completion. A saved draft only advances preparation; never mark the reply sent or the obligation waiting because a draft exists. Do not inherit the completed step's priority for a different next action. Uncertain matches use ordinary reconciliation. Report a successful external action and a failed ledger update separately.

## Rundowns and decision continuity

Apply the constitution's intake comparison and transition reconsideration rules. Link all independently closable outcomes in planning context, give selected large work a useful first finish, and distinguish prepared material from delivery. For intake, the first DCC or What's next of each day, or a material change to selected work, use the bounded decision-history procedure in sources.md; a repeat with the same selection records nothing. Where a code runtime is available, run scripts/decisions.py and its command_center.py dependency from a checkout at the bundle's commit, after checking both files' SHA-256 digests against the bundle's manifest, before validating/paging comments. Use schema 2 and the source procedure's intake mapping and check-placement operation, including renewed older tasks. A session without a runtime cannot run check-placement; that is the failed-check case in sources.md: the decision stays incomplete, verified task updates are retained, placement is never claimed verified, and the receipt says the check did not run. Fetching the scripts into a chat session does not change this. Preserve the cohort and observe/explain every selected or watched competitor. Record exact prepared recommendations separately from watch items and verified response delivery. Keep consequential displacement explanations short; never impose morning-item quotas.

## Permanent heuristic additions

For ordinary heuristic additions, show the exact proposed Markdown bullet first. Approval requires Ross's affirmative use of the standalone word `approve`, case-insensitive; a negation is not approval. Mentioning a rule does not authorize persistence.

Compare the proposed bullet with every existing heuristic for duplication and contradiction before proposing and again immediately before writing. After approval refetch main and the current heuristics blob SHA; validate the header; prepare the appended bullet and its updated runtime.json digest together. Publish both in one coherent commit based on the freshly checked parent, with no force update. If main advances, refetch and reconcile before retrying. The rule is in force only when the `verified` branch carries a bundle for that commit; until then keep using the loaded bundle and say the addition is pending release. If it is already covered, do not duplicate it; if it now conflicts, explain and resolve the conflict before persisting a changed rule. Preserve actual newlines.

An explicit instruction to implement a reviewed systems refinement authorizes necessary coherent edits within that scope under the controlling user/developer instructions; do not repeatedly ask for permission already given. It does not authorize unrelated actions or future unrequested heuristic additions.
