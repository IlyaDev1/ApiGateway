import json
from datetime import datetime
from enum import Enum

import requests  # type: ignore
from httpx import AsyncClient

from app.api.schema import SensorData, WeatherData
from app.core.repositories.psql_repo import Repo
from logger import logger

url = "http://172.16.119.197:8000"
UserURL = "http://localhost:4222/v1"


class HazardClass(Enum):
    LOW = "LOW"
    MID = "MID"
    HIGH = "HIGH"
    CRIT = "CRIT"


def to_dict(weather_data: WeatherData) -> dict:
    return {
        "wind_average": weather_data.wind_average,
        "wind_max": weather_data.wind_max,
        "temp": weather_data.temp,
        "visibility": weather_data.visibility,
        "show_depth": weather_data.snow_depth,
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
        probability = json.loads(response.content.decode("utf-8"))[
            "Avalanche probability"
        ]
        return round(float(probability), 2)
    else:
        raise Exception(
            f"Ошибка при получении прогноза. Статус: {response.status_code}, Ответ: {response.text}"
        )


async def send_message(
    sector_id: int, timestamp: datetime, forecast_value: float
):
    hazard_class: HazardClass
    if 0 < forecast_value < 0.19:
        hazard_class = HazardClass.LOW
    elif 0.2 < forecast_value < 0.39:
        hazard_class = HazardClass.MID
    elif 0.4 < forecast_value < 0.69:
        hazard_class = HazardClass.HIGH
    else:
        hazard_class = HazardClass.CRIT

    data = {
        "sector_id": sector_id,
        "timestamp": timestamp.isoformat(),
        "hazard_class": hazard_class.value,
    }

    async with AsyncClient() as async_client:
        response = await async_client.post(url=UserURL, json=data)
        if response.status_code != 200:
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

        await send_message(
            sensor_data_instance.sector_id,
            sensor_data_instance.timestamp,
            forecast_value,
        )

        return await self.repo.create_record(record_dict)
