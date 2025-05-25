import os
import argparse

# 設定ファイル
class Config:
    EXCLUDE_DIRS = {'.git', '__pycache__', '.venv'}
    EXCLUDE_FILES = {'.DS_Store'}
    SHOW_HIDDEN = False  # 隠しファイル・フォルダを表示するか

def print_tree(dir_path: str, prefix: str = ""):
    try:
        entries = list(os.scandir(dir_path))
    except PermissionError:
        print(prefix + "└─ [Permission Denied]")
        return

    # フィルタリング
    entries = [
        e for e in entries
        if (Config.SHOW_HIDDEN or not e.name.startswith('.'))
        and (e.is_dir() and e.name not in Config.EXCLUDE_DIRS or e.is_file() and e.name not in Config.EXCLUDE_FILES)
    ]

    # ディレクトリ→ファイルの順に並べ替え（名前順）
    dirs = sorted([e for e in entries if e.is_dir()], key=lambda e: e.name)
    files = sorted([e for e in entries if e.is_file()], key=lambda e: e.name)
    entries = dirs + files

    for index, entry in enumerate(entries):
        connector = "└─ " if index == len(entries) - 1 else "├─ "
        print(prefix + connector + entry.name)
        if entry.is_dir():
            extension = "    " if index == len(entries) - 1 else "│   "
            print_tree(entry.path, prefix + extension)

def main():
    parser = argparse.ArgumentParser(description="ディレクトリ構造をツリー表示します。")
    parser.add_argument("path", nargs="?", default=".", help="対象ディレクトリ (デフォルト: カレントディレクトリ)")
    args = parser.parse_args()

    root_dir = os.path.abspath(args.path)
    print(f"{root_dir}")
    print_tree(root_dir)

if __name__ == "__main__":
    main()
