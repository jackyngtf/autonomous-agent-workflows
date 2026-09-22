# Workflow reference examples

[**English**](README.md) · [繁體中文](README.zh-TW.md)

These documents explain the two reporting workflows through rewritten design references. They are not copied production runbooks and cannot connect to a live NAS. They contain no credentials or deployment configuration.

The [offline demo](../demo/README.md) is the runnable part of the portfolio. It uses synthetic inputs and local files to demonstrate checks, repeat runs and blocked updates. Its strengthened checks do not establish that every historical script implemented the same behaviour.

| Workflow | Historical purpose and schedule | Reference documents |
|---|---|---|
| Avaya call log | Daily SMDR CSVs into monthly reports; weekdays at 10:00 | [Entry](avaya-call-log/SKILL.md) · [Procedure](avaya-call-log/WORKINSTRUCTION.md) · [Synthetic report](avaya-call-log/sample-report.md) |
| NAS access log | File-transfer activity into monthly reports; weekdays at 09:00 | [Entry](nas-access-log/SKILL.md) · [Procedure](nas-access-log/WORKINSTRUCTION.md) · [Synthetic report](nas-access-log/sample-report.md) |

The procedures use `Australia/Melbourne` for date eligibility. Schedule settings, report files and successful unattended executions are different kinds of evidence.

## What you can run

From the repository root, after installing [the declared dependencies](../requirements.txt):

```sh
python -m demo --workflow all --output-dir output/demo
python -m demo --workflow all --scenario blocked --output-dir output/blocked
python -m unittest discover -s tests -v
```

The blocked scenario intentionally returns exit code 2. Each workflow writes its own report and evidence file. The demo neither contacts a NAS nor deletes source data; Avaya cleanup eligibility is a reported decision only. See the demo guide for expected artifacts and limits.

## How to read the templates

`SKILL.md` illustrates the entry instructions. `WORKINSTRUCTION.md` describes responsibilities, decision points and deployment requirements. `sample-report.md` is a fictional narrative example, not an executed run or a production evidence record. Generated demo reports are separate artifacts.

Before adapting the design, an operator must define actual permissions, source schemas, retention, publication and recovery behaviour. The templates intentionally omit live authentication snippets and credentials. They do not guarantee arbitrary Excel feature preservation or complete NAS API results.

Related: [architecture](../docs/architecture.md) · [knowledge maintenance](../docs/self-improvement-loop.md) · [portfolio](../README.md).