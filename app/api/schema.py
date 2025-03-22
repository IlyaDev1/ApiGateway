from datetime import datetime

from pydantic import BaseModel


class WeatherData(BaseModel):
    wind_average: float
    wind_max: float
    temp: float
    visibility: float
    snow_depth: float
    rainfall: float
    rainfall_per_month: float
    wind_drifting: float
    total_wind_drifting: float
    slope: float
    volume: float


class SensorData(BaseModel):
    sector_id: int
    timestamp: datetime
    weather_data: WeatherData
