from typing import Any, Dict, List
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()


class BaseModel(Base):
    """
    全てのデータモデルの基底クラス
    - 各テーブルのプライマリキーやカラム情報を取得可能にする

    SQLAlchemy のデータモデルは、`__init__` をオーバーライドしないと
    `TypeError: unexpected keyword argument` のエラーが出ることがある。


    - how to use 

    class User(Base):
        __tablename__ = "users"

        id = Column(Integer, primary_key=True)  # 主キー
        name = Column(String)                   # 名前
        email = Column(String)                  # メールアドレス

    """
    __abstract__ = True

    @classmethod
    def get_table_name(cls) -> str:
        return cls.__tablename__
    
    @classmethod
    def get_columns(cls) -> Dict[str, Dict[str, Any]]:
        return {c.name: {"type": str(c.type), "primary_key": c.primary_key} for c in cls.__table__.columns}

    @classmethod
    def get_primary_keys(cls) -> List[str]:
        return [c.name for c in cls.__table__.columns if c.primary_key]

    def to_dict(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
