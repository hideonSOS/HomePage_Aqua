import io
import re
from datetime import date, datetime

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation

from .models import Schedule


# ── 選択肢（forms.py と同じソース） ──────────────────────────────────
import json, os

def _load_title_list():
    json_path = os.path.join(os.path.dirname(__file__), 'static', 'input_page', 'js', 'title_check.json')
    with open(json_path, encoding='utf-8') as f:
        return [item[4] for item in json.load(f)]

def _load_persons_js():
    js_path = os.path.join(os.path.dirname(__file__), 'static', 'input_page', 'js', 'persons.js')
    with open(js_path, encoding='utf-8') as f:
        return f.read()

def _extract_names(content, const_name):
    block = re.search(rf'const {const_name}\s*=\s*\[(.*?)\];', content, re.DOTALL)
    if not block:
        return []
    names = re.findall(r'name:\s*"([^"]+)"', block.group(1))
    seen = set()
    return [n for n in names if not (n in seen or seen.add(n))]

def _time_list():
    times = ['']
    for h in range(6, 24):
        for m in range(0, 60, 10):
            times.append(f"{h:02d}:{m:02d}")
    return times


# ── テンプレート生成 ──────────────────────────────────────────────────
def build_template_workbook():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'スケジュール入力'

    # ── スタイル定義 ──
    hdr_fill   = PatternFill('solid', fgColor='1A237E')
    hdr_font   = Font(color='FFFFFF', bold=True, size=11)
    req_fill   = PatternFill('solid', fgColor='FFF9C4')   # 必須列（薄黄）
    opt_fill   = PatternFill('solid', fgColor='F5F5F5')   # 任意列（薄灰）
    center     = Alignment(horizontal='center', vertical='center')
    thin       = Side(border_style='thin', color='CCCCCC')
    border     = Border(left=thin, right=thin, top=thin, bottom=thin)

    # ── ヘッダー行 ──
    headers = [
        ('日付 *',               '例: 2026/07/01',            True),
        ('開催タイトル',          'GI太閤賞 など（任意）',       False),
        ('開始時刻',              '例: 09:00（任意）',           False),
        ('終了時刻',              '例: 17:00（任意）',           False),
        ('住之江ゼミナール',       '有 または 空欄',              False),
        ('前半スタジオ解説(1-6R)', '解説者名（任意）',            False),
        ('後半スタジオ解説(7-12R)','解説者名（任意）',            False),
        ('MC',                   '司会者名（任意）',             False),
        ('ゲスト',               '自由記入（任意）',             False),
    ]

    COL_DATE, COL_TITLE, COL_TSTART, COL_TEND, COL_SEMI, \
    COL_A1, COL_A2, COL_A3, COL_A4 = range(1, 10)

    # 行1: ヘッダー
    for col, (label, hint, required) in enumerate(headers, start=1):
        c = ws.cell(row=1, column=col, value=label)
        c.font   = hdr_font
        c.fill   = hdr_fill
        c.alignment = center
        c.border = border

    # 行2: ヒント行（グレー小文字）
    hint_font = Font(color='888888', italic=True, size=9)
    for col, (label, hint, required) in enumerate(headers, start=1):
        c = ws.cell(row=2, column=col, value=hint)
        c.font      = hint_font
        c.fill      = PatternFill('solid', fgColor='EEEEEE')
        c.alignment = center
        c.border    = border

    ws.row_dimensions[1].height = 22
    ws.row_dimensions[2].height = 16

    # 入力行のベーススタイル（3〜52行）
    DATA_ROWS = 50
    START_ROW = 3
    for row in range(START_ROW, START_ROW + DATA_ROWS):
        for col in range(1, 10):
            c = ws.cell(row=row, column=col)
            c.fill   = req_fill if col == COL_DATE else opt_fill
            c.border = border
            c.alignment = Alignment(horizontal='center', vertical='center')
        ws.row_dimensions[row].height = 18

    # ── データバリデーション ──
    data_range = f"A{START_ROW}:A{START_ROW + DATA_ROWS - 1}"

    # 日付: 書式設定で誘導（ExcelのDateValidationはロケール依存なのでフォーマットのみ）
    for row in range(START_ROW, START_ROW + DATA_ROWS):
        ws.cell(row=row, column=COL_DATE).number_format = 'YYYY/MM/DD'

    # 時刻: ドロップダウン（リストが255文字を超えるため隠しシートに列挙）
    ws_times = wb.create_sheet('_times')
    times = _time_list()
    for i, t in enumerate(times, start=1):
        ws_times.cell(row=i, column=1, value=t)
    ws_times.sheet_state = 'hidden'

    time_range = f"_times!$A$1:$A${len(times)}"
    for col in (COL_TSTART, COL_TEND):
        dv = DataValidation(type='list', formula1=time_range, showDropDown=False,
                            error='リストから選択してください', errorTitle='入力エラー',
                            showErrorMessage=True)
        ws.add_data_validation(dv)
        dv.sqref = f"{openpyxl.utils.get_column_letter(col)}{START_ROW}:" \
                   f"{openpyxl.utils.get_column_letter(col)}{START_ROW + DATA_ROWS - 1}"

    # ゼミナール: 「有」or空欄
    dv_semi = DataValidation(type='list', formula1='"有,"', showDropDown=False,
                             error='「有」または空欄にしてください', errorTitle='入力エラー',
                             showErrorMessage=True)
    ws.add_data_validation(dv_semi)
    dv_semi.sqref = f"E{START_ROW}:E{START_ROW + DATA_ROWS - 1}"

    # 解説者・MC: 隠しシートのリスト
    content = _load_persons_js()
    kaisetsu = [''] + _extract_names(content, 'kaisetsu')
    mc_list  = [''] + _extract_names(content, 'MC')

    ws_k = wb.create_sheet('_kaisetsu')
    for i, n in enumerate(kaisetsu, start=1):
        ws_k.cell(row=i, column=1, value=n)
    ws_k.sheet_state = 'hidden'

    ws_mc = wb.create_sheet('_mc')
    for i, n in enumerate(mc_list, start=1):
        ws_mc.cell(row=i, column=1, value=n)
    ws_mc.sheet_state = 'hidden'

    for col, sheet, names in [
        (COL_A1, '_kaisetsu', kaisetsu),
        (COL_A2, '_kaisetsu', kaisetsu),
        (COL_A3, '_mc',       mc_list),
    ]:
        dv = DataValidation(type='list',
                            formula1=f"{sheet}!$A$1:$A${len(names)}",
                            showDropDown=False,
                            error='リストから選択してください', errorTitle='入力エラー',
                            showErrorMessage=True)
        ws.add_data_validation(dv)
        dv.sqref = f"{openpyxl.utils.get_column_letter(col)}{START_ROW}:" \
                   f"{openpyxl.utils.get_column_letter(col)}{START_ROW + DATA_ROWS - 1}"

    # タイトル: 隠しシート
    titles = [''] + _load_title_list()
    ws_t = wb.create_sheet('_titles')
    for i, t in enumerate(titles, start=1):
        ws_t.cell(row=i, column=1, value=t)
    ws_t.sheet_state = 'hidden'
    dv_title = DataValidation(type='list', formula1=f"_titles!$A$1:$A${len(titles)}",
                              showDropDown=False, showErrorMessage=False)
    ws.add_data_validation(dv_title)
    dv_title.sqref = f"B{START_ROW}:B{START_ROW + DATA_ROWS - 1}"

    # ── 列幅 ──
    ws.column_dimensions['A'].width = 14
    ws.column_dimensions['B'].width = 32
    ws.column_dimensions['C'].width = 12
    ws.column_dimensions['D'].width = 12
    ws.column_dimensions['E'].width = 18
    ws.column_dimensions['F'].width = 22
    ws.column_dimensions['G'].width = 22
    ws.column_dimensions['H'].width = 16
    ws.column_dimensions['I'].width = 20

    # ── 凡例（1行目の上にメモ代わりのコメント色） ──
    ws.freeze_panes = 'A3'   # ヘッダー2行を固定

    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf


# ── インポート処理 ────────────────────────────────────────────────────
class ImportError(Exception):
    pass


def parse_and_import(file_obj, overwrite=False):
    """
    Excelを解析してScheduleを一括保存。
    Returns: (saved_count, errors_list)
    errors_list = [{'row': N, 'msg': '...'}, ...]
    """
    try:
        wb = openpyxl.load_workbook(file_obj, data_only=True)
    except Exception as e:
        raise ImportError(f'Excelファイルを開けませんでした: {e}')

    ws = wb.active
    START_ROW = 3
    errors = []
    to_save = []

    for row_idx, row in enumerate(ws.iter_rows(min_row=START_ROW, values_only=True), start=START_ROW):
        raw_date, raw_title, raw_start, raw_end, raw_semi, \
        raw_a1, raw_a2, raw_a3, raw_a4 = (row + (None,) * 9)[:9]

        # 全列空なら終了
        if all(v is None or str(v).strip() == '' for v in
               [raw_date, raw_title, raw_start, raw_end, raw_semi, raw_a1, raw_a2, raw_a3, raw_a4]):
            break

        row_errors = []

        # ── 日付 ──
        day = None
        if raw_date is None or str(raw_date).strip() == '':
            row_errors.append('日付が空です')
        else:
            if isinstance(raw_date, (date, datetime)):
                day = raw_date.date() if isinstance(raw_date, datetime) else raw_date
            else:
                s = str(raw_date).strip()
                for fmt in ('%Y/%m/%d', '%Y-%m-%d', '%Y.%m.%d'):
                    try:
                        day = datetime.strptime(s, fmt).date()
                        break
                    except ValueError:
                        pass
                if day is None:
                    row_errors.append(f'日付の形式が不正です（{raw_date}）')

        # ── 時刻 ──
        def clean_time(val):
            if val is None or str(val).strip() == '':
                return ''
            s = str(val).strip()
            if re.match(r'^\d{1,2}:\d{2}$', s):
                return s
            # Excelが小数で返す場合（0.375 = 09:00）
            try:
                f = float(s)
                total_min = round(f * 24 * 60)
                return f"{total_min // 60:02d}:{total_min % 60:02d}"
            except ValueError:
                return s

        time_start = clean_time(raw_start)
        time_end   = clean_time(raw_end)
        time_str   = f"{time_start}〜{time_end}" if (time_start or time_end) else ''

        # ── ゼミナール ──
        seminar = str(raw_semi).strip() == '有' if raw_semi else False

        # ── ゼミナールのみバリデーション ──
        title = str(raw_title).strip() if raw_title else ''
        if not title:
            if not (time_start and time_end):
                row_errors.append('タイトルなし（ゼミナールのみ）の場合は開始・終了時刻が必須です')
            if not seminar:
                row_errors.append('タイトルなし（ゼミナールのみ）の場合は住之江ゼミナール列に「有」が必要です')

        if row_errors:
            errors.append({'row': row_idx, 'msgs': row_errors})
            continue

        to_save.append({
            'day':     day,
            'title':   title,
            'time':    time_str,
            'seminar': seminar,
            'artist1': str(raw_a1).strip() if raw_a1 else '',
            'artist2': str(raw_a2).strip() if raw_a2 else '',
            'artist3': str(raw_a3).strip() if raw_a3 else '',
            'artist4': str(raw_a4).strip() if raw_a4 else '',
        })

    if errors:
        return 0, errors

    # ── 保存 ──
    saved = 0
    for d in to_save:
        if overwrite:
            Schedule.objects.update_or_create(
                day=d['day'],
                defaults={k: v for k, v in d.items() if k != 'day'}
            )
        else:
            Schedule.objects.create(**d)
        saved += 1

    return saved, []
