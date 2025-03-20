"""
Этот файл создается сам
Он отвечает за применение миграций в БД
"""

from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context  # type: ignore
from app.core.models.base import Base
from app.core.models.models import (
    FactModel,
    ForecastModel,
    MonitoringModel,
    MountainModel,
    SectorModel,
)

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

database_url = "postgresql+psycopg2://postgres:neilya1@localhost:5432/SBM?client_encoding=utf8"


config.set_main_option("sqlalchemy.url", database_url)


def run_migrations_offline() -> None:
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
