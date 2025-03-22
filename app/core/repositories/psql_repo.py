from app.core.dependencies import get_db
from app.core.models.models import ForecastModel
from logger import logger


class Repo:
    def __init__(self) -> None: ...

    async def create_record(self, data: dict) -> str:
        async with get_db() as session_instance:
            if data["forecast_value"] == 1:
                data["forecast_value"] = 0.99
            forecast = ForecastModel(
                timestamp=data["timestamp"],
                forecast_value=data["forecast_value"],
                sector_id=data["sector_id"],
            )
            session_instance.add(forecast)
            logger.info(f"{forecast} загружен в бд")
            await session_instance.flush()
            await session_instance.commit()
            return "ok"
