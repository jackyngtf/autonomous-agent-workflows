# Autonomous Agent Workflows

[English](README.md) · **繁體中文**

### 排程報表與文件換版，明確界定每一步操作

本 repo 收錄三項營運工作：PBX 通話報表、NAS 存取報表，以及 eTMS 文件換版交接。兩個報表流程由我以 Python 處理程式、書面操作程序及 Claude Cowork 執行工作階段建立。工作內容包括處理不完整輸入、保留既有紀錄、診斷失敗原因，以及留下可供覆核的執行報告。

報表案例透過三個實際營運事件說明設計決定，並以可執行的合成資料示範正常更新、重複執行及驗證失敗。eTMS 案例從全部暫緩的 shadow 執行，記錄診斷、修正測試及其後 19 項已替換的 live 結果，並對照儲存檔案與網頁提供的副本核實。

[執行離線示範](#在本機執行) · [閱讀案例](docs/case-study/01-context-and-role.zh-TW.md) · [查閱證據](docs/evidence/README.zh-TW.md)

![報表流程及獨立的 eTMS 文件換版交接](images/workflow-overview.zh-TW.svg)

*圖中呈現操作設計。歷史執行的檢查深度並不完全相同；公開示範另有明確的測試範圍。*

## 兩個報表流程

| | PBX 通話紀錄 | NAS 存取紀錄 |
|---|---|---|
| 資料來源 | [Docker 接收器](https://github.com/jackyngtf/smdr-receiver) 產生的每日 Avaya SMDR CSV | 從 NAS API 查詢的檔案傳輸紀錄 |
| 原定排程 | 平日 10:00 | 平日 09:00 |
| 輸出 | 按日期分頁的每月通話報表 | 按日期或日期組別分頁的每月存取報表 |
| 需要判斷的情況 | 拒絕格式異常輸入、調查認證失敗、選擇允許的恢復步驟 | 檢查缺漏日期、診斷 API 限制、報告無法補回的資料 |
| 資料處理 | Python 解析紀錄並重建表格式工作簿 | Python 按日期整理紀錄並重建表格式工作簿 |

以上時間是歷史紀錄中的設定，並不代表持續運作至今或目前的可用率。[查看兩條資料路徑 →](docs/case-study/02-two-reporting-workflows.zh-TW.md)

## eTMS：受限制的文件換版交接

第三項工作的入口指示設定為**平日 09:30**：檢查文件更新收件區，然後呼叫獨立的 swap driver。配對、規劃、封存、驗證及結果報告由 driver 負責；Agent 只能依照 engine 的計劃操作，遇到失敗或含糊情況必須停止。

**2026 年 9 月 22 日**已檢視設定為 **shadow**。原始碼確認 shadow 跳過正式文件替換，但仍處理收件區清理及上傳報告。只有操作負責人可以啟用 live；資料庫存取、訓練紀錄修改及臨時手動換檔，仍不在 Agent 的預期權限範圍內。

首次手動 shadow 執行將 30 項輸入全部暫緩。唯讀檢查確認，22 份被報為缺漏的目標均存在於 NAS；離線重現將問題定位至本機暫存程序。修正後，27 項輸入的重跑結果為 **19 PLANNED、8 HELD**。另一項防護修正處理含空白路徑的發布問題，完成後由操作負責人授權啟用 live。

**2026 年 9 月 23 日**，live 報告記錄 **19 SWAPPED、8 HELD**。唯讀跟進確認 19 份目的地及封存檔案均存在，19 個 HTTP 回應的 SHA-256 全部與目前 NAS 目的地一致，收件區只剩八項暫緩輸入。這八項仍需核對文件身份。尚有一項缺陷：舊檔封存名稱使用了輸入新檔的版本號；由於沒有事先擷取目的地摘要值，亦不能獨立證明備份與執行前檔案完全一致。附日期證據清楚記錄這些限制，並與報表示範及 92 份報告清單分開。

[閱讀 eTMS 案例](docs/case-study/07-etms-document-handoff.zh-TW.md) · [查閱部署與執行證據](docs/evidence/etms-deployment-review-2026-09-22.zh-TW.md) · [查看任務約定](examples/etms-doc-swap/README.zh-TW.md)

## Agent 與程式各自負責甚麼

在報表工作中，Agent 讀取操作程序、檢查目前狀態、選擇允許的動作，並解讀異常結果。Python 負責紀錄解析、日期處理、工作簿產生及明確的檢查。eTMS 約定則將寫入程序交給外置 driver。排程讓工作定期啟動；Agent 的角色是在各項工作的邊界內處理判斷與例外情況。

操作指示與可搜尋的事件歷史分開保存。有用的發現可以整理成新的操作規則，並記錄修改原因。本專案的 **self-improvement loop** 指的是這種營運知識維護，並不涉及模型訓練。

[架構與取捨](docs/architecture.zh-TW.md) · [執行環境與排程](docs/how-it-runs-in-claude-code-cowork.zh-TW.md) · [從事件到操作指示](docs/self-improvement-loop.zh-TW.md)

## 三個改變操作程序的事件

| 發生了甚麼 | 帶來的設計經驗 |
|---|---|
| 重建的 NAS 工作簿出現重複標題列，但筆數檢查仍然通過 | 若預期值來自同一條有缺陷的處理路徑，就不算獨立檢查；必須對照原有紀錄。 |
| 讀取大型工作簿超出執行時間限制 | 調整序列化的單位，再檢查輸出紀錄；把單次執行時間視為觀察值，而非效能基準。 |
| 排程環境失敗，其後目的地卻出現本機報告未記載的更新 | 規劃恢復前先重新檢查目的地，清楚標示手動恢復及來源未明的更新。 |

[閱讀事件經過與恢復決定 →](docs/case-study/04-incidents-and-recovery.zh-TW.md)

## 現有紀錄支持哪些結果

| 記載項目 | 適用範圍 |
|---|---|
| Avaya 47 份、NAS 45 份執行報告檔案 | 2026 年 9 月 22 日檢視時找到的本機檔案，排除封存副本；包含失敗及恢復報告，並非成功無人值守執行次數。 |
| 一份重建 NAS 工作簿包含 313,721 筆資料 | 記載於 2026 年 8 月 3 日；報告記錄解析 23.6 秒、寫入 22.8 秒，均為單次觀察值。 |
| NAS 新增 40,179 筆資料、四個工作表 | 記載於 2026 年 9 月 15 日的**手動／原生 Windows 恢復**；部分較舊日期仍無法從當時查詢的來源取得。 |
| Avaya 新增 21 筆資料，並檢查七個既有工作表 | 記載於 2026 年 9 月 11 日的原生環境恢復。 |

以上結果來自執行報告，並非對即時 NAS 的獨立稽核。留存資料不足以證明可用率、成功率、節省工時或零資料損失。

[操作紀錄](docs/case-study/05-operating-record.zh-TW.md) · [證據與來源邊界](docs/evidence/README.zh-TW.md) · [已知限制](docs/case-study/06-lessons-and-limitations.zh-TW.md)

## 在本機執行

使用 Python 3.11 或以上版本。兩條報表示範路徑均使用合成資料，離線執行，毋須 NAS 帳戶、Claude 工作階段或 API key。eTMS 整合只提供文件說明，這個指令不包含其私有 engine。

```bash
python -m pip install -r requirements.txt
python -m demo --workflow all --output-dir output/demo
python -m unittest discover -s tests -v
python scripts/check_docs.py
```

首次執行會在 `output/demo` 產生 Avaya 及 NAS 工作簿，另附雙語執行報告與機器可讀的驗證紀錄。再次執行相同示範指令，會回報 `NO_CHANGE`，不重寫已經相符的工作簿。

然後試一次故意修改待發布檔案的情境：

```bash
python -m demo --workflow all --scenario blocked --output-dir output/blocked
```

**預期結束代碼為 2。** 示範會發現待發布檔案不一致，阻止替換既有工作簿，並保留虛構輸入。這是在本機模擬發布前的檢查邊界，不會上傳至 NAS 或刪除來源檔案。

![由離線示範產生的合成工作簿輸出及被攔截的待發布檔案](images/demo-preview.zh-TW.svg)

[觀看合成資料示範錄影](images/demo-walkthrough.webm?raw=true) · [執行示範與驗證](demo/README.zh-TW.md)

錄影透過唯讀檢視器，查看實際產生的工作簿及受阻執行證據，標籤包含英文及繁體中文。它展示的是輸出檔案，不是正式環境 Agent 的即時執行。

## 閱讀完整案例

1. [報表需求與我的角色](docs/case-study/01-context-and-role.zh-TW.md)
2. [兩個來源、兩份每月工作簿](docs/case-study/02-two-reporting-workflows.zh-TW.md)
3. [「已驗證」需要代表甚麼](docs/case-study/03-integrity-and-verification.zh-TW.md)
4. [失敗、修改與恢復](docs/case-study/04-incidents-and-recovery.zh-TW.md)
5. [操作紀錄及其限制](docs/case-study/05-operating-record.zh-TW.md)
6. [下一步會改善甚麼](docs/case-study/06-lessons-and-limitations.zh-TW.md)
7. [eTMS：把文件修改交給受限制的 engine](docs/case-study/07-etms-document-handoff.zh-TW.md)

[參考操作指示](examples/README.zh-TW.md) 說明流程規則；[示範程式](demo/README.zh-TW.md) 則是可執行的公開參考版本。兩者都不應直接取代私有環境中的正式部署。

## 公開版本的資料邊界

本 repo 包含重新編寫的案例、經整理的來源摘要、合成輸入及本機示範程式，不包含正式環境認證資料、工作階段狀態、公司原始紀錄或即時整合介面。歷史截圖用於說明排程設定，不能證明目前排程正常運作。[媒體說明](images/README.zh-TW.md) · [安全與資料邊界](SECURITY.zh-TW.md)

公開程式及文件沿用 [MIT 授權](LICENSE)。
