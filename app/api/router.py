from fastapi import APIRouter

from app.api.schema import SensorData
from app.core.service.main_service import MainService

api_router = APIRouter()

service_instance = MainService()


@api_router.post("/")
async def handler(sensor_data_instance: SensorData):
    response = await service_instance.create_forecast_record(
        sensor_data_instance
    )
    return {"msg": response}
