import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DBInterface:
    """
    データベース接続を管理するクラス

    - `get_session()` でセッションを取得
    - SQLite など異なるデータベースでも使用可能
    """
    def __init__(self, db_url: str):
        """
        データベースの接続を初期化
        :param db_url: 接続先のデータベースURL (例: "sqlite:///test.db")
        """
    def __init__(self, db_url: str):
        try:
            self.engine = create_engine(db_url)
            self.Session = sessionmaker(bind=self.engine)
            logger.info("DB 接続成功: %s", db_url)
        except OperationalError as e:
            logger.error("DB 接続失敗: %s", e)
            raise

    def get_session(self):
        """新しいセッションを取得"""
        return self.Session()

    def create_tables(self, base):
        """テーブル作成"""
        try:
            base.metadata.create_all(self.engine)
            logger.info("テーブル作成完了")
        except SQLAlchemyError as e:
            logger.error("テーブル作成エラー: %s", e)
            raise


