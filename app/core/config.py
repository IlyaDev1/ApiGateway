"""
Конфиг приложения для портов, имен, режимов и тд
"""


class Settings:
    APP_NAME: str = "name"
    API_V1_STR: str = "/api/v1"
    DESCRIPTION: str = "SBM"
    DEBUG: str = "false"
    ASYNC_DATABASE_URL: str = (
        "postgresql+asyncpg://postgres:neilya1@localhost:5432/SBM"
    )
    APP_HOST_PORT: int = 8080


settings_instance = Settings()
