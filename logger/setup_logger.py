import logging
import copy
import sys
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

class ColoredFormatter(logging.Formatter):
    """ANSIカラー対応のフォーマッター"""
    COLORS = {
        "DEBUG": "\033[0;36m",  # CYAN
        "INFO": "\033[0;32m",  # GREEN
        "WARNING": "\033[0;33m",  # YELLOW
        "ERROR": "\033[0;31m",  # RED
        "CRITICAL": "\033[0;37;41m",  # WHITE ON RED
        "RESET": "\033[0m",  # RESET COLOR
    }

    def format(self, record):
        colored_record = copy.copy(record)
        levelname = colored_record.levelname
        seq = self.COLORS.get(levelname, self.COLORS["RESET"])
        colored_record.levelname = f"{seq}{levelname}{self.COLORS['RESET']}"
        return super().format(colored_record)

def setup_logger(
    name: str,
    numeric_level: int = logging.DEBUG,
    use_colors: bool = True,
    log_file: str = None,
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5,
    stream_level: int = logging.INFO,
    file_level: int = logging.DEBUG,
) -> logging.Logger:
    """
    汎用的なロガー設定関数

    Args:
        name (str): ロガー名
        numeric_level (int): ログレベル（ロガー全体のレベル）
        use_colors (bool): ANSIカラーを有効化するか
        log_file (str, optional): ファイル出力のパス
        max_bytes (int, optional): 1ファイルの最大サイズ
        backup_count (int, optional): ログの世代数
        stream_level (int): 標準出力のログレベル
        file_level (int): ファイル出力のログレベル

    Returns:
        logging.Logger: 設定済みのロガー
    """
    logger = logging.getLogger(name)
    logger.propagate = False

    # すでにハンドラーがある場合は再設定しない
    if logger.handlers:
        return logger
   
    # 文字列のログレベルを数値に変換
    # numeric_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(numeric_level)

    # フォーマット設定
    log_format = "[%(filename)s:%(lineno)d %(funcName)s]%(asctime)s[%(levelname)s] - %(message)s"
    date_format = "%H:%M:%S"

    # 標準出力のハンドラー
    stream_handler = logging.StreamHandler(sys.stdout)
    formatter = ColoredFormatter(log_format, datefmt=date_format) if use_colors else logging.Formatter(log_format, datefmt=date_format)
    stream_handler.setFormatter(formatter)

    stream_handler.setLevel(stream_level)

    logger.addHandler(stream_handler)

    # ファイル出力を追加（必要な場合）
    if log_file:
        log_file = os.path.abspath(log_file)
        log_dir = os.path.dirname(log_file)
        os.makedirs(log_dir, exist_ok=True)  # ディレクトリ作成
        file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8")
        file_handler.setFormatter(logging.Formatter(log_format, datefmt=date_format))

        file_handler.setLevel(file_level)

        logger.addHandler(file_handler)

    return logger

