# How It Runs: Claude Code Cowork Scheduled Tasks

The two agents in this repo don't run on cron or a serverless function. They run as **Scheduled Tasks inside Claude Code Cowork** — Anthropic's agentic coding tool — which gives a scheduled LLM agent a sandboxed filesystem, shell access, and a set of pre-approved tools, with no human present.

This doc explains the scheduling layer so you can see exactly how the three files (`SKILL.md` → `WORKINSTRUCTION.md` → `.learnings/`) plug into a real runtime, and how this setup removes repetitive work.

---

## The goal: remove a tedious daily task

Every weekday morning, two reports needed to be produced by hand. Neither had a clean "export" button that would have made them trivial:

1. **Call logs** — we needed to record who called in/out on the PBX. Commercial call-monitoring software is expensive and over-featured for simple in/out logging; [Dave Hope's free SMDR Receiver](https://davehope.co.uk/projects/smdr-receiver/) is a Windows `.exe` that would need a PC switched on 24/7. So the receiver was rebuilt as a [Docker container](https://github.com/jackyngtf/smdr-receiver) on the NAS — but that still left the daily chore of turning its CSVs into the monthly workbook. That's what this agent automates.
2. **NAS access logs** — Synology's Log Center can export logs, but only as a full dump (one "Export as HTML/CSV" button, no time-range filter). Getting one day's file-transfer activity meant exporting everything and sifting through it by hand. A dedicated syslog server was more infrastructure than the job warranted. So this agent queries the NAS's own REST API for exactly the records it needs and assembles them into the monthly workbook.

Each took a chunk of focused time every single day, on every weekday, forever — with no built-in shortcut. The goal was to make them **happen on their own at 9–10 AM**, correctly, with a paper trail — so a person never has to do it again unless something breaks.

---

## The scheduling layer: Claude Code Cowork

A Scheduled Task in Cowork is a recurring, unattended agent run. You configure five things:

| Field | What it does | Avaya example | NAS example |
|-------|-------------|---------------|-------------|
| **Instructions** | The prompt the agent starts with | The contents of `SKILL.md` | The contents of `SKILL.md` |
| **Folders** | The working directory the agent can see | `…\avaya-call-log` | `…\nas-access-log` |
| **Repeats** | The schedule | Weekdays, 10:00 | Weekdays, 09:00 |
| **Always allowed tools** | Tools the agent may use without asking (no human is present) | Bash, Read, Write, Edit | Bash, Read, Write, Edit |
| **Run history** | The result of every past run | green/red status per day | green/red status per day |

### How the files map to the task

```
┌──────────────────────────────────────────────────────────────┐
│  Claude Code Cowork Scheduled Task                           │
│                                                              │
│  Repeats: Weekdays 10:00         ← fires automatically       │
│  Always allowed tools: Bash, …   ← no human to approve       │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Instructions box  =  the contents of SKILL.md         │  │
│  │  (the entry-point contract — "read WORKINSTRUCTION.md  │  │
│  │   in full, don't read .learnings/ wholesale, …")       │  │
│  └───────────────────────────┬────────────────────────────┘  │
│                              │                               │
│  Folders: ./avaya-call-log   │  ← the working directory      │
│ ─────────────────────────────┼─────────────────────────────  │
│                              ▼                               │
│  ./SKILL.md ──────────▶ ./WORKINSTRUCTION.md ──────▶ ./.learnings/  │
│   (entry)                 (reads in full)             (grep only)  │
└──────────────────────────────────────────────────────────────┘
```

**The key decision:** the *Instructions box* in Cowork holds the **SKILL.md** content — the thin entry-point contract. It is *not* the full procedure. The SKILL.md's first instruction is "read `WORKINSTRUCTION.md` in full", so the agent loads the detailed procedure itself at run time. This keeps the scheduled-task config small and stable, while the heavy procedure lives in a file the agent can read and the human can edit.

### Why "Always allowed tools" matters

Because no human is present, the agent can't ask "can I run this command?" So the tools it needs (Bash to run Python, Read/Write/Edit for files) are pre-approved in the task. The safety comes instead from the **hard rules baked into WORKINSTRUCTION.md Section 0** — "never overwrite", "never expose credentials", "stop and report if unsure" — which the agent obeys because it read them in full at the start of the run.

---

## What a run looks like

At 10:00 on a weekday, Cowork boots a fresh agent, drops it into the working folder, feeds it the SKILL.md instructions, and lets it run with the allowed tools. The agent then:

1. **Reads `WORKINSTRUCTION.md` in full** — its complete operational ruleset
2. **Runs Step 0** — reinstalls its own Python deps (the sandbox resets between runs), checks the archive size
3. **Does the job** — discover CSVs, rebuild the workbook, upload via SMB, validate
4. **Writes a structured report** to `reports/`
5. **Appends any new lessons** to `.learnings/`
6. **Finishes** — the run shows green (or red) in Cowork's run history

Nobody is watching. If something needs a human decision (e.g. an existing sheet would need overwriting), the rule is **stop and report** — the agent writes what it *would* have done into the report and ends, rather than guessing.

---

## The run-history feedback loop

Cowork keeps a per-day history of every run (green = success, red = failure). Combined with the per-run markdown report and the append-only `.learnings/`, you get three layers of auditability:

| Layer | Where | Granularity |
|-------|-------|-------------|
| **Did the run succeed?** | Cowork run history | Pass/fail per day |
| **What exactly happened?** | `reports/*.md` | Full structured report per run |
| **Why did past failures happen, and how were they fixed?** | `.learnings/*.md` | Terse, grep-able lessons over time |

So when a run goes red, you open the report to see what broke; if it's a known issue, you grep the learnings and the fix is right there.

---

## What this replaces

Before: **a person**, every weekday morning, doing two repetitive data-shuttling tasks — pulling records, pasting into spreadsheets, uploading, checking.

After: **a scheduled agent** that does both unattended, validates its own output, writes a report, and remembers its mistakes. A person only gets involved when a run goes red or a recurring anomaly needs human judgement (e.g. investigate an external port scanner probing the PBX receiver).

That's the point: it's not a chatbot you talk to. It's a **scheduled worker that removed a daily chore**.

---

## Reproducing this with your own task

1. **Write the three files** for your task:
   - `SKILL.md` — thin entry point: where the working dir is, "read WORKINSTRUCTION.md in full", the critical safety rules, the report path
   - `WORKINSTRUCTION.md` — the complete step-by-step procedure, with a Section 0 of non-negotiable rules
   - `.learnings/` — empty `LEARNINGS.md`, `ERRORS.md`, `FEATURE_REQUESTS.md` (they grow over time)
2. **Create a Scheduled Task in Claude Code Cowork** (or any agent runtime with a scheduler + shell):
   - Paste your `SKILL.md` contents into the **Instructions** box
   - Set **Folders** to your task directory
   - Set **Repeats** to your schedule
   - Set **Always allowed tools** to what the agent needs (Bash, Read, Write, Edit)
3. **Let it run and learn.** Review the daily reports. When it makes a mistake, the lesson it logs will prevent the next run from repeating it.
