from modules.api_module import get_call_natureapi
from modules.extract_data_module import get_power_consumption, get_temperature
from modules.log_module import log_application
from modules.postgres_module import execute_query

logger = log_application(__name__)


def get_remo_data() -> None:
    url = "https://api.nature.global/1/devices"
    data = get_call_natureapi(url)

    if data is None:
        logger.error("Remoのデータ取得に失敗しました。")

    else:
        result = get_temperature(data)
        if result is None:
            logger.error("温度データの取得に失敗しました。")

        else:
            logger.info("温度データの取得に成功しました。")
            logger.info("温度: %s, 湿度: %s, 照度: %s", *result)
            # データベースに挿入
            insert_query = "SELECT temp_sensor.insert_t_temperature(%s, %s, %s);"
            with execute_query(insert_query, result) as cur:
                logger.info(cur.rowcount)


def get_remo_e_data() -> None:
    url = "https://api.nature.global/1/appliances"
    data = get_call_natureapi(url)

    if data is None:
        logger.error("Remo Eのデータ取得に失敗しました。")

    else:
        result = get_power_consumption(data)
        if result is None:
            logger.error("瞬時電力データの取得に失敗しました。")

        else:
            logger.info("瞬時電力データの取得に成功しました。")
            logger.info("瞬時電力: %s W", result)
            # データベースに挿入
            insert_query = "SELECT temp_sensor.insert_t_power_consumption(%s);"
            with execute_query(insert_query, (result,)) as cur:
                logger.info(cur.rowcount)


if __name__ == "__main__":
    logger.info("スクリプトを実行しています...")
    get_remo_data()
    get_remo_e_data()
    logger.info("処理が完了しました。")
