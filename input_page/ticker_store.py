"""
テロップ（お知らせ）テキストの保存・読み出し。

常に1件だけのため、DBは使わずプロジェクト直下のテキストファイルに保存する。
（db.sqlite3 と同じ BASE_DIR に置くので書き込み可能・再起動でも保持される）
"""
from pathlib import Path
from django.conf import settings

TICKER_FILE = Path(settings.BASE_DIR) / 'ticker_notice.txt'
MAX_LEN = 120


def get_ticker():
    """現在のテロップ文字列を返す。未設定なら空文字。"""
    try:
        return TICKER_FILE.read_text(encoding='utf-8').strip()
    except FileNotFoundError:
        return ''
    except Exception:
        return ''


def set_ticker(text):
    """テロップ文字列を保存する（前後空白除去・最大 MAX_LEN 文字に丸める）。"""
    text = (text or '').strip()[:MAX_LEN]
    TICKER_FILE.write_text(text, encoding='utf-8')
    return text
