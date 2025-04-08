import os
import json
from dataclasses import dataclass, asdict, fields
from typing import Type, Dict


# ベースクラス：ファイルの読み書きと動的属性更新
class BaseConfig:
    def __init__(self, config_dataclass: Type, config_file_path: str):
        self._config_dataclass = config_dataclass
        self._config_file_path = config_file_path

        os.makedirs(os.path.dirname(self._config_file_path), exist_ok=True)
        if not os.path.exists(self._config_file_path):
            self._save_config(config_dataclass())  # 初期値で保存

        self._load_config()

    def _load_config(self):
        with open(self._config_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        # デフォルト値に読み込んだ値を上書き
        default_config = asdict(self._config_dataclass())
        default_config.update(data)
        self.__dict__.update(default_config)

    def _save_config(self, config_instance=None):
        config_data = (
            asdict(config_instance) if config_instance else 
            {field.name: getattr(self, field.name) for field in fields(self._config_dataclass)}
        )
        with open(self._config_file_path, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=4)

    def __getitem__(self, key):
        if hasattr(self, key):
            return getattr(self, key)
        raise KeyError(f"Unknown config key: {key}")

    def __setitem__(self, key, value):
        if hasattr(self, key):
            setattr(self, key, value)
            self._save_config()
        else:
            raise KeyError(f"Unknown config key: {key}")

    def save(self):
        self._save_config()

    def reload(self):
        self._load_config()


if __name__ == "__main__" :
    pass

    # 個別の設定内容
    @dataclass
    class VideoConfig:
        SET_FRAME_RATE: int = 60
        SET_VIDEO_WIDTH: int = 1920
        SET_VIDEO_HEIGHT: int = 1080

    @dataclass
    class AudioConfig:
        SET_SAMPLE_RATE: int = 44100
        SET_CHANNELS: int = 2
        SET_BIT_DEPTH: int = 16


    # ConfigManager：複数 config のまとめ管理
    class ConfigManager:
        def __init__(self):
            self.configs: Dict[str, BaseConfig] = {}

        def register(self, name: str, config_instance: BaseConfig):
            self.configs[name] = config_instance

        def get(self, name: str) -> BaseConfig:
            return self.configs[name]

        def save_all(self):
            for config in self.configs.values():
                config.save()

        def reload_all(self):
            for config in self.configs.values():
                config.reload()
