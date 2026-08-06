# Architecture Deep Dive

The three-layer architecture exists to solve one core tension in autonomous LLM agents: **they need rich operational context to run safely, but context windows are finite.** You cannot hand an agent a 100 KB procedure and 200 KB of historical lessons every run. This pattern keeps the always-read layer small and pushes history into a search-only layer.

## Layer 1 — `SKILL.md` (entry point)

The thinnest file. Its only job is to tell the agent:

1. **Where the working directory is**
2. **That `WORKINSTRUCTION.md` is the complete operational ruleset — read it in full**
3. **That `.learnings/` is append-only and must only be consulted via `grep`, never read wholesale**
4. **The report path and required report sections**
5. **A handful of the most critical safety rules** (so they're visible even before the work-instruction is read)

It is intentionally short (≈50 lines). A scheduler invokes the agent with the skill as its starting context. Because it only points at the other files, it almost never changes — which keeps the scheduler contract stable.

### Why not put everything in the skill?

Because the skill is what the runtime loads first. If it's huge, every run pays that token cost even for the parts that only matter on error. The skill defers to the work-instruction for procedure and to the archive for history.

## Layer 2 — `WORKINSTRUCTION.md` (operational truth)

The authoritative, always-read ruleset. This is the only file the agent reads **in full** every run. It contains:

- **Section 0 — Critical Rules** — the non-negotiable safety invariants (no credential exposure, no overwrites, export-only-up-to-yesterday, validate-twice, stop-and-report)
- **Section 1 — Overview** — what the task does, end to end
- **Connection parameters** — redacted to vault references in the sanitized version
- **Step-by-step procedure** — Step 0 (pre-flight + self-heal dependencies) through Step N (generate report), plus conditional steps (month-end consolidation)
- **Reference implementation** — the actual Python snippets (SMB connect with keyword args, `xlsxwriter` rebuild, validation)

### How it evolves

When the agent learns something that **changes how the task should run**, it edits this file. That is the only way an operational rule changes. The edit is always accompanied by an append-only archive entry (the audit trail of *why* the rule changed and when).

### Self-healing dependencies

A notable production reality: the runtime VM's filesystem resets between scheduled runs. Each Step 0 re-installs its own dependencies (`pysmb`, `holidays`) before doing anything else. The agent does not assume yesterday's environment still exists.

## Layer 3 — `.learnings/` (append-only archive)

Four files, never rewritten, only appended to:

| File | Content |
|------|---------|
| `LEARNINGS.md` | Operational insights that don't quite rise to a work-instruction edit (e.g. "this NAS returns `STATUS_INVALID_PARAMETER` for `createDirectory` on an existing folder") |
| `ERRORS.md` | Errors hit and how they were resolved (e.g. "curl fails on `entry.cgi` with error 105 — use Python `requests`") |
| `FEATURE_REQUESTS.md` | Improvements noticed but not yet promoted |
| `archive/` | Entries older than 90 days, rotated here by month-end consolidation |

### The grep-only rule

The cardinal rule of this layer: **never read these files wholesale during a run.** They exist to be searched, not loaded. The skill and work-instruction both repeat this instruction. Reading them wholesale would bloat the context window and, worse, risk the agent treating a superseded entry as current truth.

Instead, when the agent hits an error or an uncertain decision, it runs a targeted grep:

```bash
grep -rn "smb" .learnings/      # SMB connection failed
grep -rn "nul\|encoding" .learnings/   # CSV won't parse
grep -rn "auth" .learnings/     # NAS auth failed
```

This keeps the archive's value high (it's comprehensive) while keeping its cost low (it's only consulted when needed).

## How the three layers interact

```
   ┌──────────────┐
   │  SKILL.md    │  loaded by scheduler — points downward
   └──────┬───────┘
          │ "read WORKINSTRUCTION.md in full"
          ▼
   ┌──────────────────────┐
   │  WORKINSTRUCTION.md  │  read in full every run — the truth
   └──────┬───────────────┘
          │ on error only: "grep .learnings/"
          ▼
   ┌──────────────────────┐
   │  .learnings/*.md     │  append-only — the audit trail
   └──────────────────────┘
```

**Writes flow the other way, after the run:**

- A novel error → append to `.learnings/ERRORS.md`
- A novel insight → append to `.learnings/LEARNINGS.md`
- If it changes operations → *also* edit `WORKINSTRUCTION.md`

The archive entry is the history; the work-instruction edit is the living rule. Together they give the agent both memory and a single source of operational truth.

## Why not just use a vector database?

For this scale (a single task's operational knowledge, growing ~tens of entries/month), grep over markdown is simpler, fully transparent (you can read the archive in a text editor), version-controlled (it's in git), and has zero infrastructure. The agent can reason about a grep hit in its full original prose. A vector DB would add a retrieval service, embeddings cost, and opaque ranking — for no benefit at this volume. The pattern is deliberately boring infrastructure.
