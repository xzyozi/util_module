import logging
from typing import Generic, Type, TypeVar, List
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

T = TypeVar("T")  

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChangeTracker(Generic[T]):
    """
    データの変更を追跡・管理するクラス

    - inserts: 新規追加するレコード
    - updates: 更新するレコード
    - deletes: 削除するレコード

    バルク処理を行い、データベースへまとめて適用できる。
    """
    def __init__(self, model_class: Type[T]) -> None:
        self.model_class = model_class
        
        # バッファ（変更適用後クリア）
        self.current_inserts: List[T] = []
        self.current_updates: List[T] = []
        self.current_deletes: List[T] = []

        # 全変更履歴（クリアされない）
        self.all_inserts: List[T] = []
        self.all_updates: List[T] = []
        self.all_deletes: List[T] = []

    def add_insert(self, obj: T):
        """新規レコードの追加"""
        self.current_inserts.append(obj)

    def add_update(self, obj: T):
        """更新レコードの追加"""
        self.current_updates.append(obj)

    def add_delete(self, obj: T):
        """削除レコードの追加"""
        self.current_deletes.append(obj)

    def bulk_apply(self, session: Session):
        """
        変更をまとめてデータベースに適用
        - `merge()` を使用して insert と update を統合
        - 失敗しても例外を投げず、ログを出力し処理を継続
        """

        logger.info(
            f"変更適用開始: inserts={len(self.current_inserts)}, "
            f"updates={len(self.current_updates)}, deletes={len(self.current_deletes)}"
        )

        try:
            # `merge()` を使用して insert と update を統合
            for obj in self.current_inserts + self.current_updates:
                session.merge(obj)
            self.all_inserts.extend(self.current_inserts)
            self.all_updates.extend(self.current_updates)

            # 削除処理
            for obj in self.current_deletes:
                try:
                    session.delete(obj)
                except SQLAlchemyError as e:
                    logger.error(f"削除失敗: {obj} → {e}")

            self.all_deletes.extend(self.current_deletes)

            session.commit()
            logger.info("変更を適用しました")

        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"変更の適用に失敗しました: {e}")

        finally:
            # バッファをクリア
            self.current_inserts.clear()
            self.current_updates.clear()
            self.current_deletes.clear()
            session.close()