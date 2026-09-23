# 媒體與重製說明

[English](README.md) · **繁體中文** · [作品集](../README.zh-TW.md)

| 檔案 | 呈現內容 |
|---|---|
| `workflow-overview.svg` 及 `.zh-TW.svg` | 重新繪製的報表架構，加上 eTMS 原始碼檢視與手動 shadow 結果摘要；不是擷取的執行追蹤。 |
| `demo-preview.svg` 及 `.zh-TW.svg` | 根據實際合成工作簿尺寸及受阻執行紀錄繪製的預覽；不是正式環境截圖。 |
| [demo-walkthrough.webm](demo-walkthrough.webm?raw=true) | 32 秒瀏覽器錄影，查看產生的唯讀檔案檢視器：Avaya 工作表、NAS 紀錄及受阻結果；標籤包含英文與繁體中文。 |
| `cowork-avaya-task-detail.png`、`cowork-nas-task-detail.png` | 沿用原有公開 repo 的歷史排程設定遮蔽截圖；不能證明目前執行環境正常。 |

先執行正常示範及另一目錄中的受阻示範，再執行以下指令重製新圖：

```bash
python scripts/render_portfolio_media.py
```

程式從 `output/demo/` 及 `output/blocked/` 讀取合成預覽資料，確認預期結果類別後產生四份 SVG。架構圖亦包含按[附日期 eTMS 證據說明](../docs/evidence/etms-deployment-review-2026-09-22.zh-TW.md)撰寫的彙總文字，不會取得部署資料。圖中沒有私人文件紀錄、外部託管字型或追蹤程式。SVG 文字提供英文與繁體中文版本，README 亦附有描述性的替代文字。

要重製錄影中的檢視器，可執行 `python scripts/render_demo_walkthrough.py`，再用瀏覽器開啟 `output/demo-walkthrough.html`。檢視器嵌入由實際 XLSX 檔讀取的部分欄列，顯示前先將檔案雜湊與證據核對。它是錄影輔助工具，不是正式應用程式；本 repo 的錄影以 1440 × 1024 解析度，由瀏覽器內實際點擊這個檢視器而成。
