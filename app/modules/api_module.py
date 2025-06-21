import requests

from modules.log_module import log_application
from settings.config import settings

logger = log_application(__name__)


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
