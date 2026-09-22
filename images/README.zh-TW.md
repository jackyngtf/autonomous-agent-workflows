# 媒體與重製說明

[English](README.md) · **繁體中文** · [作品集](../README.zh-TW.md)

| 檔案 | 呈現內容 |
|---|---|
| `workflow-overview.svg` 及 `.zh-TW.svg` | 重新繪製的架構圖，說明預期操作邊界；不是歷史執行追蹤。 |
| `demo-preview.svg` 及 `.zh-TW.svg` | 根據實際合成工作簿尺寸及受阻執行紀錄繪製的預覽；不是正式環境截圖。 |
| `cowork-avaya-task-detail.png`、`cowork-nas-task-detail.png` | 沿用原有公開 repo 的歷史排程設定遮蔽截圖；不能證明目前執行環境正常。 |

先執行正常示範及另一目錄中的受阻示範，再執行以下指令重製新圖：

```bash
python scripts/render_portfolio_media.py
```

程式只讀取 `output/demo/` 及 `output/blocked/`，確認預期結果類別後，產生四份 SVG。圖中沒有外部託管字型、追蹤程式或正式環境紀錄。SVG 文字提供英文與繁體中文版本，README 亦附有描述性的替代文字。
