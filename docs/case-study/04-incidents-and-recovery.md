# 04 · Incidents and recovery

[English](04-incidents-and-recovery.md) · [繁體中文](04-incidents-and-recovery.zh-TW.md) · [Project overview](../../README.md)

Three incidents explain why the procedure changed. Dates and figures below are reported observations, with source locators in the [evidence index](../evidence/claim-index.md).

## June 25: a plausible result failed content comparison

The NAS rebuild duplicated headers. Its row-count check initially passed because both the output and expected count shared the same mistake. A content comparison caught the shifted records before upload.

The procedure gained an explicit header-skip rule and a count check against a fresh read of the original file. The useful improvement was a more independent verification path.

## July–August: fitting a growing workbook into the runtime

A July 31 parse timed out near 274,000 existing rows while serializing individual rows. The recovery used separate chunk files. The subsequent preferred path serialized each worksheet as a unit.

On August 3, the report records a single parse of 295,332 existing rows, including headers, in 23.6 seconds. Writing 313,721 data rows across 27 sheets took 22.8 seconds. These are observations from one run, not a controlled benchmark or a general speedup claim.

There was also an earlier emergency package-assembly workaround that conflicted with the standing reconstruction rule. That exception remained documented for review; the history does not support a claim that every run followed every invariant.

## September: recovery started by checking what already existed

Workspace failures prevented some scheduled sessions from reaching the data systems. The September 11 Avaya abort report and later Windows-native recovery report are separate artifacts. The recovery added 21 call rows after inspecting seven existing worksheets.

The September 15 NAS recovery was explicitly manual and Windows-native. It discovered that another session had already exported more data than local reports suggested, then added 40,179 rows in four new worksheets.

Some August dates were no longer retrievable through the live API. The recovery left their gaps visible. Other retained records showed that the destination could contain more history than the API still exposed. The source's estimated retention duration conflicts with its dated observations, so this case study makes no fixed retention-window claim.

## What changed in the operating approach

The recovery evidence reinforces four decisions: stop early when the environment cannot run; re-inspect destination coverage; preserve unknown provenance rather than invent attribution; and distinguish a completed export from partial historical recovery.

A future version should also record execution IDs and external publication provenance centrally. Local report filenames cannot establish what happened in sessions that left no local report.

[Previous](03-integrity-and-verification.md) · [Next: operating record](05-operating-record.md)
