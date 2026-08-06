# Autonomous Agent Workflows

> Architecture & patterns for **production-grade, self-improving AI agents that run unattended on a schedule.**

This repo documents a pattern I use in production to run LLM-powered agents as **scheduled, fully autonomous tasks** — no human in the loop. Two real agents built on this pattern have run **daily for 60+ consecutive days**, exporting call logs and file-transfer logs to monthly Excel workbooks on a NAS, learning from their own mistakes along the way.

It is not a framework or a library. It is a **repeatable file-and-prompt architecture** that works with any agent runtime that can read files and run shell commands (Claude Code / ZCode, etc.).

---

## Why this matters

Most "AI automation" is a person pasting prompts into a chatbot. That doesn't run at 9 AM on its own, and it doesn't get better over time. This pattern does both:

- **Unattended** — triggered by a scheduler. A skill file is the entry point. No user is present.
- **Safe by design** — hard rules prevent destructive actions (overwrite, delete, expose credentials).
- **Self-improving** — every run logs errors and insights to an append-only archive; future runs consult it via targeted search before repeating a mistake.
- **Self-maintaining** — a month-end consolidation pass merges duplicates, prunes stale entries, and promotes durable lessons into the operational rulebook.

---

## The three-layer architecture

```
                    ┌─────────────────────────────────────────┐
   Scheduler ─────▶ │  SKILL.md        (entry point)          │
  (daily 9/10 AM)   │  the minimal "how to start" contract    │
                    └────────────────────┬────────────────────┘
                                         │ read in full
                                         ▼
                    ┌─────────────────────────────────────────┐
                    │  WORKINSTRUCTION.md  (operational truth) │
                    │  step-by-step procedure + critical rules │
                    │  THIS is the authoritative ruleset       │
                    └────────────────────┬────────────────────┘
                                         │ consult on errors only
                                         ▼
                    ┌─────────────────────────────────────────┐
                    │  .learnings/       (append-only archive) │
                    │  LEARNINGS.md  ERRORS.md  FEATURE_*.md   │
                    │  grep-only — NEVER read wholesale        │
                    └─────────────────────────────────────────┘
```

| Layer | File | Read when | Written when |
|-------|------|-----------|--------------|
| **Entry** | `SKILL.md` | Every run (start) | Rarely — stable contract |
| **Truth** | `WORKINSTRUCTION.md` | Every run (in full) | When an operational rule changes |
| **Archive** | `.learnings/*.md` | **Only via `grep`** on error/uncertainty | After every run (append-only) |

The key insight: **the archive is for audit, the work-instruction is for operations.** New knowledge gets written to *both* — the archive entry is the history, the work-instruction edit is the living rule. Future runs read the work-instruction wholesale but only *search* the archive, so the archive can grow without bloating the context window.

📖 Deep dive: [`docs/architecture.md`](docs/architecture.md)

---

## The self-improvement loop

```
  run starts ──▶ works from WORKINSTRUCTION.md
       │
       │ hits error / novel situation
       ▼
  grep .learnings/ ──▶ found prior lesson? ──yes──▶ apply it, continue
       │ no
       ▼
  solve it this run
       │
       ▼
  post-run: append TERSE entry to .learnings/ERRORS.md or LEARNINGS.md
       │
       ▼ (if it changes how the task should run)
  also edit WORKINSTRUCTION.md — promote the lesson to an operational rule
```

### Month-end consolidation

On the **last working day** of each month (Mon–Fri, excluding public holidays — computed deterministically with the `holidays` package), the agent runs an extra pass on its own knowledge base:

1. Merge duplicate entries across `LEARNINGS.md` / `ERRORS.md` / `FEATURE_REQUESTS.md`
2. Prune entries superseded by a newer lesson
3. Promote any newly-durable operational rule into `WORKINSTRUCTION.md`
4. Rotate old entries (90+ days) into `.learnings/archive/`
5. Emit its own `learnings_consolidation_report_YYYY-MM-DD.md`

A consolidation failure is isolated — it never affects the already-completed daily export. A missed trigger day carries forward with an **idempotent-per-month catch-up**, so a missed day never skips a whole month.

📖 Deep dive: [`docs/self-improvement-loop.md`](docs/self-improvement-loop.md)

---

## Reference implementations

Two sanitized, production-derived examples are included. All IPs, hostnames, share paths, and credentials have been redacted.

| Agent | Schedule | Job | Example |
|-------|----------|-----|---------|
| **avaya-call-log** | Weekdays 10 AM | Read SMDR CSVs from a Dockerized PBX receiver, rebuild a monthly Excel workbook with `xlsxwriter`, upload via SMB, validate, clean up | [`examples/avaya-call-log/`](examples/avaya-call-log/) |
| **nas-access-log** | Weekdays 9 AM | Fetch file-transfer logs from a Synology NAS via REST API, rebuild a monthly Excel workbook, upload via SMB, validate | [`examples/nas-access-log/`](examples/nas-access-log/) |

Each example contains a sanitized `SKILL.md` (the entry point), a trimmed `WORKINSTRUCTION.md` (the procedure), and a `sample-report.md` showing the structured output every run produces.

---

## Safety invariants baked into every run

These are non-negotiable rules written into every `WORKINSTRUCTION.md` Section 0:

- **Never expose credentials** — passwords/tokens go in a vault, never in a report or `.md`
- **Never overwrite** existing data without explicit approval — only *create new* entries
- **Export only up to yesterday** (Melbourne/AEST) — today's data may be incomplete
- **Never delete** a processed input until its output is confirmed in the uploaded file
- **Validate twice** — rebuild locally *and* re-download from the NAS after upload
- **Stop and report** on any ambiguity that would need human approval — don't guess

---

## Results in production

- ✅ 60+ unattended daily runs per agent, across two agents
- ✅ Self-healing dependencies (the runtime VM's filesystem resets between runs; each run re-installs its own `pysmb` / `holidays`)
- ✅ Detects and tracks recurring anomalies (e.g. corrupted CSVs from an external port scanner) without crashing — flagged as stale items across 41 consecutive runs
- ✅ Month-end consolidation runs on schedule with cross-month catch-up
- ✅ Every run emits a structured markdown report (run summary, export table, skipped items, open questions)

---

## Tech stack

`Python` · `xlsxwriter` · `pysmb` (SMB upload) · `requests` (Synology REST API) · `holidays` (deterministic business-day logic) · Docker (SMDR receiver) · markdown-driven agent runtime

---

## License

MIT — the architecture and patterns here are free to adapt. The reference implementations are sanitized excerpts from production work.
