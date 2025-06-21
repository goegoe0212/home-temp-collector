from modules.log_module import log_application

logger = log_application(__name__)


def get_temperature(data: dict) -> tuple | None:
    """データから温度を取得する関数"""
    temperature = None
    humidity = None
    illuminance = None
    try:
        # 温度データを取得
        device_info = next((device for device in data if device.get("name") == "Remo"), None)
        if not device_info:
            logger.error("Remoデバイスが見つかりません。")
            return None

        newest_events = device_info.get("newest_events", {})
        temperature = newest_events.get("te", {}).get("val")
        humidity = newest_events.get("hu", {}).get("val")
        illuminance = newest_events.get("il", {}).get("val")

    except Exception:
        logger.exception("温度データの変換に失敗しました。")
        return None

    return temperature, humidity, illuminance


def get_power_consumption(data: dict) -> int | None:
    """データからスマートメーターの瞬時電力(W)を取得する関数"""
    power_watt = None
    try:
        # スマートメータータイプのデバイスを抽出
        smart_meter = next((device for device in data if device.get("type") == "EL_SMART_METER"), None)
        if not smart_meter:
            logger.error("スマートメーターが見つかりません。")
            return None

        # echonetlite_propertiesから瞬時電力を取得
        properties = smart_meter.get("smart_meter", {}).get("echonetlite_properties", [])
        instantaneous = next((prop for prop in properties if prop.get("name") == "measured_instantaneous"), None)
        if not instantaneous:
            return None

        # valは文字列なのでintに変換
        power_watt = int(instantaneous.get("val"))

    except Exception:
        logger.exception("電力データの取得に失敗しました。")
        return None

    return power_watt
