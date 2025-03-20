from app.core.dependencies import get_db
from app.core.models.models import ForecastModel


class Repo:
    def __init__(self) -> None: ...

    async def create_record(self, data: dict) -> str:
        async with get_db() as session_instance:
            forecast = ForecastModel(
                timestamp=data["timestamp"],
                forecast_value=data["forecast_value"],
                sector_id=data["sector_id"],
            )
            session_instance.add(forecast)
            await session_instance.flush()
            await session_instance.commit()
            return "ok"
