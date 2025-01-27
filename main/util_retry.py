import time
import traceback
import traceback
from functools import wraps

def retry_func(tries=3, exceptions=(Exception,), delay=3, backoff=2):
    """
    関数をリトライするデコレータ。

    Args:
        tries: 最大リトライ回数。デフォルトは3。
        exceptions: リトライ対象の例外のタプル。デフォルトは(Exception,)。
        delay: リトライ間の遅延時間（秒）。デフォルトは3。
        backoff: 遅延の増加率。デフォルトは2（指数関数的遅延）。

    Returns:
        デコレートされた関数。
    """
    def retry_decorator(func):
        @wraps(func)  # 元の関数の情報を保持
        def wrapper(*args, **kwargs):
            m_tries, m_delay = tries, delay
            for attempt in range(m_tries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    print(f"関数 '{func.__name__}' の実行に失敗しました (試行 {attempt + 1}/{m_tries}): {e}")
                    print(traceback.format_exc()) # デバッグログとしてトレースバックを出力
                    if attempt < m_tries - 1:
                        time.sleep(m_delay)
                        m_delay *= backoff  # 遅延を増加
                else:
                    logger.info(f"関数 '{func.__name__}' の実行に成功しました。")
                    return # 成功したら即時return
            else:
                print(f"関数 '{func.__name__}' は最大試行回数に達しました。")
                raise Exception(f"関数 '{func.__name__}' は最大試行回数に達しました。処理を中断します.") # 変更点: 関数名をエラーメッセージに含める
        return wrapper
    return retry_decorator