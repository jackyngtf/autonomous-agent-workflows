# 流程參考範例

[English](README.md) · [**繁體中文**](README.zh-TW.md)

這些文件以重新編寫的設計參考，解釋兩個報表流程及一個 eTMS 文件替換交接流程。它們不是直接複製的正式操作手冊，也不能連接正式系統，不包含憑證或部署設定。

[離線示範](../demo/README.zh-TW.md)才是作品集中可執行的部分。它以合成輸入及本機檔案展示 Avaya 與 NAS 報表的檢查、重跑及阻止有問題的更新。示範加強後的檢查，不代表每個歷史程式都實作了相同行為。eTMS 的 [2026 年 9 月 22 日部署檢視](../docs/evidence/etms-deployment-review-2026-09-22.zh-TW.md)以唯讀方式檢查私有 driver、engine 及 shadow 設定，沒有執行它們。檢視區分預期約定與程式缺口。另行評估的手動 shadow 報告記錄 30 項暫緩，沒有已規劃或已替換項目；離線檢查及其後核實的部署分開記錄，修正後的 Cowork 執行仍待觸發。

| 流程 | 歷史用途與排程 | 參考文件 |
|---|---|---|
| Avaya 通話紀錄 | 將每日 SMDR CSV 整理成月報；平日 10:00 | [入口](avaya-call-log/SKILL.zh-TW.md) · [程序](avaya-call-log/WORKINSTRUCTION.zh-TW.md) · [合成報告](avaya-call-log/sample-report.zh-TW.md) |
| NAS 存取紀錄 | 將檔案傳輸活動整理成月報；平日 09:00 | [入口](nas-access-log/SKILL.zh-TW.md) · [程序](nas-access-log/WORKINSTRUCTION.zh-TW.md) · [合成報告](nas-access-log/sample-report.zh-TW.md) |
| eTMS 文件替換 | 排程交接至外置 engine；入口指引指定平日 09:30 | [證據邊界](etms-doc-swap/README.zh-TW.md) · [入口](etms-doc-swap/SKILL.zh-TW.md) · [程序](etms-doc-swap/WORKINSTRUCTION.zh-TW.md) |

兩個報表程序以 `Australia/Melbourne` 計算日期資格。eTMS 來源沒有指定排程時區。排程設定、報告檔案與成功的無人值守執行，是不同種類的證據。

## 可以執行的內容

在 repository 根目錄安裝[指定依賴](../requirements.txt)後執行：

```sh
python -m demo --workflow all --output-dir output/demo
python -m demo --workflow all --scenario blocked --output-dir output/blocked
python -m unittest discover -s tests -v
```

Blocked 情境會刻意回傳結束碼 2。每個流程產生獨立報告及證據檔案。示範不連接 NAS，也不刪除來源資料；Avaya 清理資格只是一項記錄下來的判斷。預期產出及限制詳見示範指南。

## 如何閱讀範本

`SKILL.md` 展示入口指引。`WORKINSTRUCTION.md` 描述責任、決策點及部署要求。Avaya 與 NAS 的 `sample-report.md` 是虛構敘事範例，不是曾經執行的結果或正式環境證據。程式產生的示範報告屬於另外的產出。eTMS 記錄已檢視的部署程式及限制，不虛構成功執行：shadow 會跳過正式文件替換，但仍處理收件區清理及上傳報告；driver 回傳零結束碼也不代表 engine 成功。

套用設計前，操作負責人需要訂明實際權限、來源結構、保留政策、發佈及恢復行為。範本刻意不包含真實驗證程式及憑證，也不保證保留任意 Excel 功能，或 NAS API 回傳完整資料。

相關文件：[架構](../docs/architecture.zh-TW.md) · [知識維護](../docs/self-improvement-loop.zh-TW.md) · [作品集](../README.zh-TW.md)。
