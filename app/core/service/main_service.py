import json

import requests  # type: ignore

from app.api.schema import SensorData, WeatherData
from app.core.repositories.psql_repo import Repo

url = "http://172.16.119.197/"


def to_dict(weather_data: WeatherData) -> dict:
    return {
        "wind_average": weather_data.wind_average,
        "wind_max": weather_data.wind_max,
        "temp": weather_data.temp,
        "visibility": weather_data.visibility,
        "show_depth": weather_data.show_depth,
        "rainfall": weather_data.rainfall,
        "rainfall_per_month": weather_data.rainfall_per_month,
        "total_wind_drifting": weather_data.total_wind_drifting,
        "wind_drifting": weather_data.wind_drifting,
        "slope": weather_data.slope,
        "volume": weather_data.volume,
    }


def get_forecast(weather_data: WeatherData) -> float:
    weather_data_json = json.dumps(to_dict(weather_data))
    headers = {"Content-Type": "application/json"}

    response = requests.get(url, data=weather_data_json, headers=headers)

    if response.status_code == 200:
        return float(response.json())
    else:
        raise Exception(
            f"Ошибка при получении прогноза. Статус: {response.status_code}, Ответ: {response.text}"
        )


class MainService:
    def __init__(self):
        self.repo = Repo()

    async def create_forecast_record(self, sensor_data_instance: SensorData):
        forecast_value: float = get_forecast(sensor_data_instance.weather_data)
        record_dict = {
            "sector_id": sensor_data_instance.sector_id,
            "timestamp": sensor_data_instance.timestamp,
            "forecast_value": forecast_value,
        }
        return self.repo.create_record(record_dict)
