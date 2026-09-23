# 03 · Integrity and verification

[English](03-integrity-and-verification.md) · [繁體中文](03-integrity-and-verification.zh-TW.md) · [Project overview](../../README.md)

The critical question is whether the output contains the intended records and preserves existing ones. Opening an XLSX file successfully answers only a small part of that question.

## The preservation contract

These workbooks contain structured operational tables. Reconstruction writes a replacement monthly file with existing records and additional worksheets. “Preserve existing data” refers to the agreed tabular content; the remote workbook file is replaced during publication. This is not a general promise to preserve arbitrary Excel drawings, formulas, macros, or package bytes.

The design separates several checks:

| Boundary | What to establish |
|---|---|
| Input | Expected schema, valid records, eligible dates, and explicit treatment of malformed data |
| Original workbook | Readable file, known worksheet coverage, independently obtained counts and content |
| Rebuilt workbook | Expected names, order, counts, dates, and preserved values |
| Published copy | Downloaded output agrees with the expected workbook |
| Source cleanup | Publication checks succeeded for that specific input |

Historical validation depth varied. The table is the design contract; each evidence entry states which checks its source actually records.

## A count check can share the same bug

On June 25, a NAS reconstruction included the old header as a data row, then wrote a new header above it. The “original” row count was derived using the same incorrect assumption, so counts appeared to agree. Content comparison exposed the repeated header and shifted data.

The recorded fix skipped the original header and compared against a fresh read of the original workbook. The lesson is to obtain expected values independently enough to challenge the transformation. The report states that upload waited until the defect was corrected. See **NAS-20260625** in the [selected narratives](../evidence/selected-run-extracts/README.md).

## Checks must match the claim

The September 15 NAS helper checks every sheet's row count, samples two existing rows, and checks the first and last dates of most new sheets. Only the small weekend sheet receives a complete date scan. That supports a narrower statement than “every cell was verified unchanged.”

Likewise, matching worksheet names alone cannot prove that a published workbook contains all expected records. A reusable implementation should explicitly compare the values required by its contract, distinguish a missing file from a failed read, and stop when an API batch might be truncated.

The public offline demo uses synthetic data to make checks reviewable. Its behavior is separate evidence from the historical deployment, and its local publication simulation does not verify a real SMB transfer.

[Previous](02-two-reporting-workflows.md) · [Next: incidents and recovery](04-incidents-and-recovery.md)
