# 06 · Lessons and limitations

[English](06-lessons-and-limitations.md) · [繁體中文](06-lessons-and-limitations.zh-TW.md) · [Project overview](../../README.md)

The most useful outcome was a clearer operating procedure: what evidence permits an update, what must be checked independently, and which conditions require stopping.

## Decisions I would retain

- **Use deterministic code for stable rules.** Date calculations, schema checks, grouping, and value comparisons should be explicit and testable. Agent judgment is most useful around exceptions and diagnosis.
- **Inspect the destination before planning recovery.** Local history can be incomplete while other sessions have already published results.
- **Make missing data visible.** Retaining a malformed file or reporting an unavailable date is more informative than silently generating a plausible workbook.
- **Separate incident history from current instructions.** Search detailed history when relevant; keep the operating procedure focused on current rules.
- **Treat publication and cleanup as separate decisions.** A successful local reconstruction does not establish that the published copy is correct.

## Boundaries in the current evidence

Historical reports were written during execution and are not independent audit attestations. Validation evolved and sometimes used samples. Some reports contradict later observations; their uncertainty remains visible in the [evidence notes](../evidence/README.md).

Knowledge consolidation can rewrite or prune working notes. Calling those files permanently append-only would overstate their audit properties. A durable audit trail requires preserving the original versions or an immutable event history.

The September recovery helpers contain session-specific dates and assumptions. They are evidence of how a recovery was performed, not a deployable general-purpose orchestration library. The public demo is a separate, local implementation using synthetic data.

## What I would improve next

| Improvement | Reason |
|---|---|
| Stable execution IDs and centralized run history | Reconcile scheduled, manual, blocked, and externally completed work. |
| Named timezone and daylight-saving tests | Replace historical fixed UTC+10 snippets with actual Melbourne rules. |
| Strict API completeness handling | A full-size batch must trigger narrower queries or a stop, rather than a warning alone. |
| Defined workbook comparison contract | Establish exactly which values and metadata must survive reconstruction. |
| Versioned operating instructions and incident records | Preserve the reason for a change without treating mutable notes as immutable evidence. |
| Explicit recovery ownership and source retention | Set escalation and recovery expectations using verified system settings. |

These are engineering priorities, not claims that the historical deployment already satisfies them. Improvements demonstrated in the offline code must still be validated in the real integration environment before deployment.

[Previous](05-operating-record.md) · [Evidence index](../evidence/README.md) · [Project overview](../../README.md)
