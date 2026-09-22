# Workflow reference examples

[**English**](README.md) · [繁體中文](README.zh-TW.md)

These documents explain two reporting workflows and an eTMS document-replacement handoff through rewritten design references. They are not copied production runbooks and cannot connect to live systems. They contain no credentials or deployment configuration.

The [offline demo](../demo/README.md) is the runnable part of the portfolio. It covers Avaya and NAS reporting with synthetic inputs and local files to demonstrate checks, repeat runs and blocked updates. Its strengthened checks do not establish that every historical script implemented the same behaviour. For eTMS, a [22 September 2026 deployment review](../docs/evidence/etms-deployment-review-2026-09-22.md) inspected the private driver, engine and shadow configuration without executing them. The review distinguishes the intended contract from source-level gaps. A separately assessed, user-triggered shadow report records 30 held inputs and no planned or swapped items; offline checks and the later verified deployment are recorded separately, alongside the later manual shadow result: 19 PLANNED, 8 HELD and 0 SWAPPED on a 27-input subset of the earlier 30.

| Workflow | Historical purpose and schedule | Reference documents |
|---|---|---|
| Avaya call log | Daily SMDR CSVs into monthly reports; weekdays at 10:00 | [Entry](avaya-call-log/SKILL.md) · [Procedure](avaya-call-log/WORKINSTRUCTION.md) · [Synthetic report](avaya-call-log/sample-report.md) |
| NAS access log | File-transfer activity into monthly reports; weekdays at 09:00 | [Entry](nas-access-log/SKILL.md) · [Procedure](nas-access-log/WORKINSTRUCTION.md) · [Synthetic report](nas-access-log/sample-report.md) |
| eTMS document replacement | Scheduled handoff to an external engine; entry instructions specify weekdays at 09:30 | [Evidence boundary](etms-doc-swap/README.md) · [Entry](etms-doc-swap/SKILL.md) · [Procedure](etms-doc-swap/WORKINSTRUCTION.md) |

The two reporting procedures use `Australia/Melbourne` for date eligibility. The eTMS source does not specify its schedule timezone. Schedule settings, report files and successful unattended executions are different kinds of evidence.

## What you can run

From the repository root, after installing [the declared dependencies](../requirements.txt):

```sh
python -m demo --workflow all --output-dir output/demo
python -m demo --workflow all --scenario blocked --output-dir output/blocked
python -m unittest discover -s tests -v
```

The blocked scenario intentionally returns exit code 2. Each workflow writes its own report and evidence file. The demo neither contacts a NAS nor deletes source data; Avaya cleanup eligibility is a reported decision only. See the demo guide for expected artifacts and limits.

## How to read the templates

`SKILL.md` illustrates the entry instructions. `WORKINSTRUCTION.md` describes responsibilities, decision points and deployment requirements. The Avaya and NAS `sample-report.md` files are fictional narrative examples, not executed runs or production evidence records. Generated demo reports are separate artifacts. eTMS documents inspected deployment code and its limitations, without inventing a successful run: shadow skips production-document swaps but still performs inbox housekeeping and report uploads, and a zero driver exit does not establish engine success.

Before adapting the design, an operator must define actual permissions, source schemas, retention, publication and recovery behaviour. The templates intentionally omit live authentication snippets and credentials. They do not guarantee arbitrary Excel feature preservation or complete NAS API results.

Related: [architecture](../docs/architecture.md) · [knowledge maintenance](../docs/self-improvement-loop.md) · [portfolio](../README.md).
