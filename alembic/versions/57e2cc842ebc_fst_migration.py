"""fst migration

Revision ID: 57e2cc842ebc
Revises: 9d578b29442e
Create Date: 2025-03-19 09:52:48.914304

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op  # type: ignore

# revision identifiers, used by Alembic.
revision: str = "57e2cc842ebc"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Создание таблицы "mountain"
    op.create_table(
        "mountain",
        sa.Column(
            "id",
            sa.Integer(),
            autoincrement=True,
            nullable=False,
            primary_key=True,
        ),
        sa.Column("name", sa.String(length=127), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_mountain_id"), "mountain", ["id"])

    # Создание таблицы "sector"
    op.create_table(
        "sector",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("lower_level", sa.Integer(), nullable=False),
        sa.Column("top_level", sa.Integer(), nullable=False),
        sa.Column(
            "cardinal_point",
            sa.Enum(
                "NORTH",
                "EAST",
                "SOUTH",
                "WEST",
                "NORTHEAST",
                "SOUTHEAST",
                "SOUTHWEST",
                "NORTHWEST",
                name="cardinal_point_enum",
            ),
            nullable=False,
        ),
        sa.Column("mountain_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["mountain_id"], ["mountain.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_check_constraint(
        "ck_sector_lower_level_positive", "sector", sa.text("lower_level > 0")
    )
    op.create_check_constraint(
        "ck_sector_top_level_greater_than_lower",
        "sector",
        sa.text("top_level > lower_level"),
    )
    op.create_index(op.f("ix_sector_id"), "sector", ["id"], unique=False)

    # Создание таблицы "fact"
    op.create_table(
        "fact",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("is_avalanche", sa.Boolean(), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.Column("sector_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["sector_id"], ["sector.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_fact_id"), "fact", ["id"], unique=False)
    op.create_index(
        op.f("ix_fact_timestamp"), "fact", ["timestamp"], unique=False
    )

    # Создание таблицы "forecast"
    op.create_table(
        "forecast",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.Column(
            "forecast_value", sa.Numeric(precision=2, scale=2), nullable=False
        ),
        sa.Column("sector_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["sector_id"], ["sector.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_forecast_id"), "forecast", ["id"], unique=False)
    op.create_index(
        op.f("ix_forecast_timestamp"), "forecast", ["timestamp"], unique=False
    )

    # Создание таблицы "monitoring"
    op.create_table(
        "monitoring",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.Column("sector_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["sector_id"], ["sector.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_monitoring_id"), "monitoring", ["id"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_monitoring_id"), table_name="monitoring")
    op.drop_table("monitoring")
    op.drop_index(op.f("ix_forecast_timestamp"), table_name="forecast")
    op.drop_index(op.f("ix_forecast_id"), table_name="forecast")
    op.drop_table("forecast")
    op.drop_index(op.f("ix_fact_timestamp"), table_name="fact")
    op.drop_index(op.f("ix_fact_id"), table_name="fact")
    op.drop_table("fact")
    op.drop_index(op.f("ix_sector_id"), table_name="sector")
    op.drop_table("sector")
    op.drop_index(op.f("ix_mountain_id"), table_name="mountain")
    op.drop_table("mountain")
