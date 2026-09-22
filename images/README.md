# Media and reproduction notes

**English** · [繁體中文](README.zh-TW.md) · [Portfolio](../README.md)

| Asset | What it shows |
|---|---|
| `workflow-overview.svg` and `.zh-TW.svg` | Authored architecture diagram of the intended operating boundaries; not a historical execution trace. |
| `demo-preview.svg` and `.zh-TW.svg` | Designed preview derived from the actual synthetic workbook dimensions and blocked-run evidence. Not a production screenshot. |
| `cowork-avaya-task-detail.png`, `cowork-nas-task-detail.png` | Existing redacted historical task-configuration captures retained from the earlier public repository. Not evidence of current runtime health. |

Recreate the new graphics from a successful demo and a separate blocked demo, then run:

```bash
python scripts/render_portfolio_media.py
```

The script reads only `output/demo/` and `output/blocked/`, checks the expected outcome classes, and writes the four SVGs. The graphics use no externally hosted fonts, tracking scripts or production records. SVG text is available in English and Traditional Chinese; the README supplies descriptive alternative text.
