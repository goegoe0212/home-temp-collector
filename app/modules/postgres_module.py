from collections.abc import Generator
from contextlib import contextmanager

import psycopg

from modules.log_module import log_application
from settings.config import settings

logger = log_application(__name__)


@contextmanager
def get_connection() -> Generator:
    """接続管理用のコンテキストマネージャ"""
    conn = None
    dsn = (
        f"dbname={settings.postgresql_dbname} "
        f"user={settings.postgresql_user} "
        f"password={settings.postgresql_password} "
        f"host={settings.postgresql_host} "
        f"port={settings.postgresql_port}"
    )
    try:
        conn = psycopg.connect(dsn)
        logger.info("データベースに正常に接続しました")
        yield conn
    except Exception:
        logger.exception("データベース接続に失敗しました")
        raise
    finally:
        if conn:
            conn.close()
            logger.info("データベース接続を閉じました")


@contextmanager
def execute_query(query: str, params: tuple = ()) -> Generator:
    """クエリ実行用のコンテキストマネージャ

    Args:
        query: 実行するSQLクエリ
        params: クエリパラメータ
        transaction: トランザクション管理を行うか

    """
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                with conn.transaction():
                    cur.execute(query, params)
                    yield cur

                logger.info("クエリが正常に実行されました: %s", query)

        except Exception:
            logger.exception("クエリ実行に失敗しました: %s", query)
            conn.rollback()
            raise
