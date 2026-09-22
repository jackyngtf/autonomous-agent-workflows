# Selected run narratives

[English](README.md) · [繁體中文](README.zh-TW.md) · [Evidence guide](../README.md) · [Project overview](../../../README.md)

These are sanitized summaries written for the portfolio, not verbatim report copies. Figures retain their original units and dates. Private source basenames match the [ledger](../run-ledger.csv); exact source ranges appear in the [claim index](../claim-index.md).

## AVA-20260615 · Verification before cleanup

The report describes adding 14 call records to a workbook that already held 182 records across eight worksheets. Before reconstruction, the existing-sheet parser was compared with a separate workbook reader using names, counts, and row signatures. After upload, the downloaded workbook contained nine worksheets and 196 data rows.

Only the successfully processed source file was deleted. A malformed input and the current day's input remained. This is a concrete example of treating cleanup as a gated step. The report's post-upload evidence concerns names and counts; it does not describe a second complete cell comparison after publication.

## NAS-20260625 · Two matching counts were both wrong

The first reconstruction duplicated each existing worksheet's header. The derived expected count shared that off-by-one error, so the count check falsely passed. A content spot-check revealed the repeated header and shifted rows.

The parser was corrected to skip the original header. Counts were then checked against a fresh read of the original workbook, with additional content comparisons. The report states that no file was uploaded before correction. This incident motivates independent validation; it is not evidence that all historical validation was complete.

## NAS-20260803 · Changing the serialization unit

An earlier run had timed out while serializing each row separately. On August 3, serialization used one object per worksheet. The report records 23.6 seconds to parse 295,332 existing rows including headers, followed by 22.8 seconds to write 313,721 data rows across 27 worksheets.

The same session created a new-month workbook containing 706 data rows. The old-month addition was 18,415 rows. Local and downloaded-copy validation were recorded. The timings describe that session's environment; no controlled speedup ratio is inferred.

## AVA-20260810 · Valid additions, malformed inputs retained

The scheduled report records two new worksheets containing 16 and 20 data rows. Two known malformed files were skipped and retained for review. The record therefore supports 36 added rows and continuing exception handling, not resolution of those malformed sources.

## AVA-20260911 · A blocked session and a separate recovery

The scheduled-session report records an unavailable execution environment, no connection to the NAS, no worksheet additions, and no source deletions. A separate report from later that day records Windows-native execution, inspection of seven existing worksheets, and one new worksheet containing 21 call rows.

The destination already contained data that the local reporting history had not accounted for. Its prior exporter was unknown. The native report establishes the recovery environment; it does not establish an unattended scheduler trigger. Both artifacts remain separate in the ledger.

## NAS-20260914 and NAS-20260915 · Recoverable data and visible gaps

On September 14, the scheduled session stopped before authentication because the workspace could not execute commands. A later vendor error message identified a September workspace blocker, but the report correctly observed that the earlier August failure period predated that explanation.

The September 15 report explicitly describes a manual Windows-native recovery. Destination inspection found that another session had already exported some data. The recovery added 40,179 records in four worksheets while retaining the existing eight worksheets' row counts. Local checks and a downloaded-copy check were reported.

August 28–30 could no longer be retrieved through the live API, and no empty worksheets were created to disguise the gap. The report also described partial availability of other dates. It did not establish a verified retention setting or prove that no separate archive could support later recovery.

The source claims broad content preservation, but the inspected helper performs all-sheet count checks and two existing-row samples. Most new-sheet dates are checked at the boundaries; the small weekend sheet is scanned completely. This narrative therefore reports those checks at their actual scope.
