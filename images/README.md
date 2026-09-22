# Media and reproduction notes

**English** · [繁體中文](README.zh-TW.md) · [Portfolio](../README.md)

| Asset | What it shows |
|---|---|
| `workflow-overview.svg` and `.zh-TW.svg` | Authored reporting architecture plus a summary of the eTMS source review and manual shadow result; not a captured execution trace. |
| `demo-preview.svg` and `.zh-TW.svg` | Designed preview derived from the actual synthetic workbook dimensions and blocked-run evidence. Not a production screenshot. |
| [demo-walkthrough.webm](demo-walkthrough.webm?raw=true) | 32-second browser recording of the generated, read-only artifact viewer: Avaya sheets, NAS records and the blocked result. English and Traditional Chinese labels. |
| `cowork-avaya-task-detail.png`, `cowork-nas-task-detail.png` | Existing redacted historical task-configuration captures retained from the earlier public repository. Not evidence of current runtime health. |

Recreate the new graphics from a successful demo and a separate blocked demo, then run:

```bash
python scripts/render_portfolio_media.py
```

The script reads `output/demo/` and `output/blocked/` for the synthetic preview, checks the expected outcome classes, and writes four SVGs. The architecture diagram also contains authored aggregate text from the [dated eTMS evidence note](../docs/evidence/etms-deployment-review-2026-09-22.md); it does not fetch deployment data. The graphics contain no private document records, externally hosted fonts or tracking scripts. SVG text is available in English and Traditional Chinese; the README supplies descriptive alternative text.

To recreate the recording's viewer, run `python scripts/render_demo_walkthrough.py`, then open `output/demo-walkthrough.html` in a browser. The viewer embeds selected columns and rows read from the generated XLSX files; it checks their hashes against the evidence before displaying results. It is a recording aid, not a production application. The committed recording was captured at 1440 × 1024 by clicking through this viewer in a browser.
