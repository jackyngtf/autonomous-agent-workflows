"""Render bilingual SVGs for reporting design, synthetic outputs and eTMS evidence.

Run normal and blocked demos first. The eTMS caption is an authored aggregate.
No network or raw private operational input.
"""
from html import escape
import json
from pathlib import Path
import openpyxl

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'images'
INK, MUTED, GREEN, LINE = '#183632', '#586760', '#16735a', '#cfd8cf'


def start(title, desc, height=700):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{height}" viewBox="0 0 1200 {height}" role="img" aria-labelledby="title desc">',
            f'<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>',
            '<style>text{font-family:Inter,Segoe UI,Microsoft JhengHei,Noto Sans CJK TC,sans-serif} .mono{font-family:Consolas,monospace}</style>',
            f'<rect width="1200" height="{height}" fill="#f5f6f0"/>']


def text(parts, x, y, value, size=19, color=INK, weight=400, klass=''):
    parts.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}" class="{klass}">{escape(str(value))}</text>')


def box(parts, x, y, w, h, fill='#ffffff'):
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{LINE}"/>')


def line(parts, x1, y1, x2, y2, color=GREEN):
    parts.append(f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="{color}" stroke-width="2"/>')


def save(parts, filename):
    OUT.mkdir(exist_ok=True)
    (OUT / filename).write_text('\n'.join(parts + ['</svg>']) + '\n', encoding='utf-8')


def architecture(zh):
    title = '每次更新，都經過明確的檢查' if zh else 'Every update has a boundary.'
    p = start(title, 'Reporting design and the eTMS post-fix shadow report: 19 planned, 8 held, zero swapped. A separate live-publication defect remains unresolved in deployment.', 930)
    text(p, 48, 48, 'AUTONOMOUS AGENT WORKFLOWS', 14, GREEN, 700)
    text(p, 48, 104, title, 38, INK, 650)
    text(p, 48, 144, '排程啟動工作；Agent 解讀情況；Python 處理及比較資料。' if zh else 'A schedule starts the session. The agent interprets. Python processes and compares.', 20, MUTED)
    labels = [
        ('01 / 輸入' if zh else '01 / INPUTS', 'Avaya · 每日 CSV' if zh else 'Avaya · daily CSV', 'NAS · API 紀錄' if zh else 'NAS · API records', '只處理完整日期' if zh else 'Completed dates only'),
        ('02 / 規劃' if zh else '02 / PLAN', '檢查既有工作簿' if zh else 'Inspect the workbook', '辨識缺漏與衝突' if zh else 'Find gaps and conflicts', '不明情況保持可見' if zh else 'Keep uncertainty visible'),
        ('03 / 重建' if zh else '03 / REBUILD', 'Python + XlsxWriter', '保留支援的紀錄' if zh else 'Retain supported records', '產生待發布檔案' if zh else 'Write a candidate'),
        ('04 / 驗證' if zh else '04 / VERIFY', '獨立讀取及比較' if zh else 'Read and compare', '核對傳輸後副本' if zh else 'Check the received copy', '發布前停止異常更新' if zh else 'Stop mismatched updates')]
    for i, (k, a, b, c) in enumerate(labels):
        x = 48 + i * 282
        box(p, x, 204, 258, 194)
        text(p, x+20, 242, k, 14, GREEN, 700)
        text(p, x+20, 287, a, 19, INK, 600)
        text(p, x+20, 322, b, 18)
        text(p, x+20, 366, c, 16, MUTED)
        if i < 3:
            line(p, x+258, 301, x+276, 301)
            p.append(f'<path d="M{x+271} 296 L{x+277} 301 L{x+271} 306" fill="none" stroke="{GREEN}" stroke-width="2"/>')
    box(p, 48, 442, 540, 120, '#e6eee5')
    box(p, 612, 442, 540, 120, '#f4eade')
    text(p, 72, 479, '通過 → 發布並記錄結果' if zh else 'PASS → publish and record the outcome', 22, GREEN, 650)
    text(p, 72, 519, 'Avaya 清理來源前，必須確認驗證結果。' if zh else 'Avaya cleanup depends on a verified result.', 18)
    text(p, 636, 479, '失敗 → 保留輸入、停止並報告' if zh else 'FAIL → retain inputs, stop and report', 22, '#865023', 650)
    text(p, 636, 519, '不要把資料缺漏或不明來源當作成功。' if zh else 'A gap or unknown source stays visible.', 18)
    text(p, 48, 618, '事件 → 搜尋歷史 → 修改操作指示' if zh else 'Incident → searchable history → revised operating instructions', 22, INK, 600)
    text(p, 48, 658, '操作設計；歷史檢查深度不一。離線 demo 另有測試範圍。' if zh else 'Operating design. Historical checks varied; the offline demo has a separate tested scope.', 17, MUTED)
    box(p, 48, 700, 1104, 185)
    text(p, 72, 738, '第三項工作 / eTMS 文件換版交接' if zh else 'THIRD JOB / eTMS document-update handoff', 20, GREEN, 650)
    text(p, 72, 779, '外置 driver · Shadow：19 PLANNED / 8 HELD / 0 SWAPPED' if zh else 'External driver · shadow: 19 PLANNED / 8 HELD / 0 SWAPPED', 22, INK, 600)
    text(p, 72, 819, '2026-09-22 16:35 手動重跑 · 27 份輸入，未釐清配對保持 HELD。' if zh else '22 Sep 2026, 16:35 manual rerun · 27 inputs; unresolved identities stay held.', 18)
    text(p, 72, 858, 'Shadow 規劃已驗證；live 發布仍有缺陷，尚未執行換檔。' if zh else 'Shadow planning observed. A live-publication defect remains; no swaps performed.', 17, MUTED)
    save(p, 'workflow-overview.zh-TW.svg' if zh else 'workflow-overview.svg')


def preview(zh):
    records = {}
    for workflow in ('avaya', 'nas'):
        base = ROOT / 'output' / 'demo' / workflow
        evidence = json.loads((base/'evidence.json').read_text(encoding='utf-8'))
        blocked = json.loads((ROOT/'output'/'blocked'/workflow/'evidence.json').read_text(encoding='utf-8'))
        if evidence['status'] not in ('PUBLISHED', 'NO_CHANGE') or blocked['status'] != 'BLOCKED':
            raise RuntimeError('Run successful and blocked demos before rendering.')
        attempts = blocked.get('workbooks', [])
        if not blocked.get('input_unchanged') or not attempts:
            raise RuntimeError('Blocked evidence must prove the fixture input remained unchanged.')
        for attempt in attempts:
            if (attempt.get('status') != 'BLOCKED'
                    or not attempt.get('reason', '').startswith('Workbook content mismatch:')
                    or not attempt.get('workbook_sha256_before')
                    or attempt.get('workbook_sha256_before') != attempt.get('workbook_sha256_after')
                    or attempt.get('cleanup_executed') is not False
                    or attempt.get('cleanup_eligible_dates') != []):
                raise RuntimeError('Blocked evidence must prove content rejection and retention before rendering.')
        book = openpyxl.load_workbook(base/'2026-08.xlsx', read_only=True)
        try:
            sheets = [(s.title, s.max_row-1, s.max_column) for s in book.worksheets]
        finally:
            book.close()
        records[workflow] = (sheets, blocked['input_unchanged'])
    title = '一個完成的更新，一個被阻止的更新' if zh else 'One update accepted. One stopped.'
    p = start(title, 'Designed preview derived from generated synthetic workbooks and blocked-run evidence; not a production screenshot.', 650)
    text(p, 48, 48, 'OFFLINE DEMO / SYNTHETIC DATA', 14, GREEN, 700)
    text(p, 48, 101, title, 36, INK, 650)
    text(p, 48, 142, '依據實際 demo 輸出繪製；不含正式環境資料。' if zh else 'Rendered from actual demo outputs. No production records.', 20, MUTED)
    for i, workflow in enumerate(('avaya', 'nas')):
        x = 48 + i*564
        box(p, x, 186, 540, 244)
        text(p, x+24, 223, workflow.upper()+' / 2026-08.xlsx', 21, INK, 650)
        text(p, x+24, 264, '工作表' if zh else 'Worksheet', 16, MUTED)
        text(p, x+300, 264, '資料筆數' if zh else 'Data rows', 16, MUTED)
        text(p, x+432, 264, '欄數' if zh else 'Columns', 16, MUTED)
        for j, (name, rows, cols) in enumerate(records[workflow][0]):
            y=303+j*40
            line(p,x+24,y-25,x+516,y-25,LINE)
            text(p,x+24,y,name,19,INK,400,'mono')
            text(p,x+324,y,rows,21,INK,600)
            text(p,x+448,y,cols,21,INK,600)
        total=sum(s[1] for s in records[workflow][0])
        text(p,x+24,397,(f'合共 {total} 筆 · 保留前一日紀錄' if zh else f'{total} total records · previous day retained'),18,GREEN,600)
    box(p,48,462,1104,118,'#f4eade')
    text(p,72,501,'BLOCKED / '+('內容差異被攔截' if zh else 'changed cell detected'),22,'#865023',650)
    text(p,72,540,'原工作簿保留 · 輸入未變 · 未執行清理 · exit 2' if zh else 'Prior workbook retained · input unchanged · cleanup not executed · exit 2',19,INK)
    text(p,48,620,'本機傳輸模擬；不是 NAS 上傳或正式環境截圖。' if zh else 'Local transfer simulation. This is not a NAS upload or a production screenshot.',17,MUTED)
    save(p,'demo-preview.zh-TW.svg' if zh else 'demo-preview.svg')


if __name__ == '__main__':
    for translated in (False, True):
        architecture(translated)
        preview(translated)
    print('Rendered four bilingual SVGs from synthetic demo outputs.')
