# The Self-Improvement Loop

How an agent that starts each run with no memory of the previous run **still gets better over time.**

## The problem

LLM agents are stateless between sessions. A run at 9 AM has no memory of what went wrong at 9 AM yesterday. Without a deliberate mechanism, the agent repeats the same mistakes forever.

## The mechanism: write everything, read selectively

Every run, after completing (or failing), **appends** anything genuinely new to the archive:

```
post-run:
  if NEW error occurred:
      append one-line rule + 1-2 lines detail to .learnings/ERRORS.md
  if NEW insight occurred:
      append to .learnings/LEARNINGS.md
  if insight changes HOW the task runs:
      ALSO edit WORKINSTRUCTION.md   ← promote to operational rule
```

The word **append** is load-bearing. History is never rewritten. An entry that turns out to be wrong isn't deleted — it's superseded by a newer entry, and the old one eventually gets pruned by month-end consolidation. This gives a full audit trail of how the agent's understanding evolved.

## Reading: targeted grep, never wholesale

The complement to "write everything" is "read almost nothing." During a run, the archive is consulted only when the agent hits a problem:

```
run hits error
    │
    ▼
grep -rn "<keyword>" .learnings/
    │
    ├─ hit found → apply the prior lesson, continue
    │
    └─ no hit → solve it fresh this run
                 then append the new lesson post-run
```

This is why the archive can grow without hurting performance: it's only ever read a few lines at a time, via search.

### Example entries (sanitized)

```markdown
### SMB createDirectory returns STATUS_INVALID_PARAMETER on existing folder
This Synology NAS returns 0xC000000D for createDirectory on an already-existing
folder. Treat createDirectory failure as non-fatal — re-listPath and proceed;
storeFile fails loudly if the folder is genuinely missing.
See: WORKINSTRUCTION.md Step 5

### curl fails on entry.cgi with error 105
Use Python requests for ALL entry.cgi API calls. curl fails with error 105.
Do NOT pass enable_syno_token when authenticating.
```

Each entry is a terse rule first, optional detail second, and a `See:` pointer to the work-instruction if it was promoted. That structure makes grep hits immediately actionable.

## Month-end consolidation

Left alone, an append-only archive only grows. Once a month, the agent cleans its own house. On the **last working day** of the month — computed deterministically (Mon–Fri minus public holidays via the `holidays` package, `subdiv='VIC'`) — an extra pass runs:

1. **Merge duplicates** across `LEARNINGS.md`, `ERRORS.md`, `FEATURE_REQUESTS.md`
2. **Prune superseded entries** — if entry B says "the real fix for X is Y, not Z as in entry A," entry A goes
3. **Promote durable rules** — any operational lesson that's been relied on gets distilled into `WORKINSTRUCTION.md`
4. **Rotate** entries older than 90 days into `.learnings/archive/` (still grep-able, just out of the active set)
5. **Emit a report** — `reports/learnings_consolidation_report_YYYY-MM-DD.md`

### Failure isolation

A consolidation failure **must not** affect the already-completed daily export. The consolidation is documents-only — it never touches the NAS or workbooks. So if it fails, the worst case is a slightly cluttered archive until next month, not a corrupted production artifact.

### The catch-up: idempotent per month

The trigger check is `is_last_working_day_of_month(today)`. But what if the scheduler is down that day? The logic carries forward:

```
the newest month that is "due" = today is on/after its last workday
if this month isn't due yet, the previous month is the newest due one
run exactly once per month-window:
    only if the eligible month is newer than the last completed one
```

A missed day never skips a whole month. The next time the agent runs after the last workday, it picks up the due consolidation. And because the check is idempotent per month (gated on "newer than last done"), it can't double-run.

## What this achieves

- **No repeated mistakes** — a solved error is a grep away from being solved again, instantly
- **Graceful degradation** — the agent doesn't need to be perfect on first encounter; it just needs to record well enough to be perfect on second encounter
- **Self-maintaining knowledge** — no human curates the archive; the agent prunes and promotes on its own schedule
- **Full auditability** — because nothing is deleted (only superseded/rotated), you can reconstruct the entire learning history of the task
