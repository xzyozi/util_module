from dataclasses import dataclass, field, fields
from typing import Any, Dict, List, Type, TypeVar 
from sqlalchemy.sql import text

T = TypeVar('T', bound='BaseModel')

@dataclass
class BaseModel:
    """
    全てのデータモデルの基底クラス
    - 各テーブルのプライマリキーやカラム情報を取得可能にする

    - how to use 

    @dataclass
    class User(BaseModel):
        id: int = field(metadata={"sql_type": "INTEGER", "primary_key": True})
        name: str = field(metadata={"sql_type": "TEXT"})
        age: int = field(metadata={"sql_type": "INTEGER"})
        email: str = field(metadata={"sql_type": "TEXT"})

    """
    @classmethod
    def get_table_name(cls) -> str:
        """テーブル名を取得"""
        return cls.__name__.lower()

    @classmethod
    def get_columns(cls) -> Dict[str, Dict[str, Any]]:
        """カラムの構造を取得"""
        columns = {}
        for field_info in fields(cls):
            columns[field_info.name] = {
                "type": field_info.type,
                "metadata": field_info.metadata,
            }
        return columns

    @classmethod
    def get_primary_keys(cls) -> List[str]:
        """プライマリキーを取得"""
        return [
            field_info.name
            for field_info in fields(cls)
            if field_info.metadata.get("primary_key", False)
        ]

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        """辞書からモデルインスタンスを生成"""
        return cls(**data)

    def to_dict(self, exclude_none: bool = False) -> Dict[str, Any]:
        """インスタンスの辞書化（Noneを除外可能）"""
        if exclude_none:
            return {k: v for k, v in self.__dict__.items() if v is not None}
        return self.__dict__.copy()

    def generate_insert_sql(self) -> str:
        """INSERT文の生成（安全なSQLAlchemy構文）"""
        data = self.to_dict()
        columns = ", ".join(data.keys())
        placeholders = ", ".join(f":{key}" for key in data.keys())
        return str(text(f"INSERT INTO {self.get_table_name()} ({columns}) VALUES ({placeholders})"))

    def generate_update_sql(self) -> str:
        """UPDATE文の生成（プライマリキー必須）"""
        data = self.to_dict()
        primary_keys = self.get_primary_keys()
        if not primary_keys:
            raise ValueError(f"{self.__class__.__name__} にはプライマリキーが定義されていません。")

        columns = ", ".join(f"{key} = :{key}" for key in data.keys() if key not in primary_keys)
        where_clause = " AND ".join(f"{pk} = :{pk}" for pk in primary_keys)

        return str(text(f"UPDATE {self.get_table_name()} SET {columns} WHERE {where_clause}"))

    def generate_delete_sql(self) -> str:
        """DELETE文の生成（プライマリキー必須）"""
        primary_keys = self.get_primary_keys()
        if not primary_keys:
            raise ValueError(f"{self.__class__.__name__} にはプライマリキーが定義されていません。")

        where_clause = " AND ".join(f"{pk} = :{pk}" for pk in primary_keys)

        return str(text(f"DELETE FROM {self.get_table_name()} WHERE {where_clause}"))
