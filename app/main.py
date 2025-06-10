import logging

import psycopg
import requests

from settings.config import settings

logger = logging.getLogger(__name__)


def get_call_natureapi(api_url: str) -> dict | None:
    """Nature APIを呼び出す関数"""
    data = None
    try:
        # Header情報を設定
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {settings.nature_api_key}",
        }

        # GETリクエストを送信
        response = requests.get(api_url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

    except requests.exceptions.HTTPError:
        logger.exception("HTTPエラーが発生しました")
    except requests.exceptions.ConnectionError:
        logger.exception("接続エラーが発生しました")
    except requests.exceptions.Timeout:
        logger.exception("タイムアウトエラーが発生しました")
    except requests.exceptions.RequestException:
        logger.exception("予期せぬエラーが発生しました")

    return data


def get_temperature(data: dict) -> tuple | None:
    """データから温度を取得する関数"""
    temperature = None
    humidity = None
    illuminance = None
    try:
        # 温度データを取得
        device_info = data[0]  # 最初のデバイス情報を取得
        newest_events = device_info.get("newest_events", {})
        temperature = newest_events.get("te", {}).get("val")
        humidity = newest_events.get("hu", {}).get("val")
        illuminance = newest_events.get("il", {}).get("val")

    except Exception:
        logger.exception("温度データの変換に失敗しました。")
        return None

    return temperature, humidity, illuminance


def post_to_db(temperature: float, humidity: float, illuminance: int) -> None:
    """データをPostgreSQLデータベースに保存する関数"""
    # 接続情報を適宜設定
    dsn = (
        f"dbname={settings.postgresql_dbname} "
        f"user={settings.postgresql_user} "
        f"password={settings.postgresql_password} "
        f"host={settings.postgresql_host} "
        f"port={settings.postgresql_port}"
    )

    with psycopg.connect(dsn) as conn, conn.cursor() as cur:
        try:
            cur.execute(
                "SELECT temp_sensor.insert_t_temperature(%s, %s, %s);",
                (temperature, humidity, illuminance),
            )
            conn.commit()
            logger.info("データベースに関数が正常に呼び出されました。")
        except Exception:
            logger.exception("データベースへの挿入に失敗しました")
            conn.rollback()


if __name__ == "__main__":
    logger.info("スクリプトを実行しています...")
    url = "https://api.nature.global/1/devices"
    data = get_call_natureapi(url)

    if data is None:
        logger.error("データの取得に失敗しました。")
    else:
        result = get_temperature(data)
        if result is None:
            logger.error("温度データの取得に失敗しました。")
        else:
            temperature, humidity, illuminance = result
            post_to_db(temperature, humidity, illuminance)
    logger.info("処理が完了しました。")
