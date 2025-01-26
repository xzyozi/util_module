from dataclasses import dataclass, field, fields
from typing import Any, Dict, List, Type, TypeVar 

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
        """
        フィールド情報を取得し、カラムの構造を定義
        Returns:
            {フィールド名: {型情報、メタ情報}}
        """
        columns = {}
        for field_info in fields(cls):
            col_name = field_info.name
            col_type = field_info.type
            metadata = field_info.metadata
            columns[col_name] = {
                "type": col_type,
                "metadata": metadata,
            }
        return columns

    @classmethod
    def get_primary_keys(cls) -> List[str]:
        """
        プライマリキーとして指定されたフィールド名を取得
        """
        return [
            field_info.name
            for field_info in fields(cls)
            if field_info.metadata.get("primary_key", False)
        ]

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        """
        辞書からモデルインスタンスを生成
        """
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        """インスタンスの辞書化"""
        return {k: v for k, v in self.__dict__.items()}
    
