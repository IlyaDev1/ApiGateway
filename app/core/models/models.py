from enum import Enum as PyEnum

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import relationship

from app.core.models.base import Base


class CardinalPoint(PyEnum):
    """
    Класс-перечисление для хранения сторон света
    """

    NORTH = "North"
    EAST = "East"
    SOUTH = "South"
    WEST = "West"
    NORTHEAST = "Northeast"
    SOUTHEAST = "Southeast"
    SOUTHWEST = "Southwest"
    NORTHWEST = "Northwest"


class MountainModel(Base):
    """
    Эта модель отвечает за таблицу с названиями гор
    """

    __tablename__ = "mountain"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(length=127), unique=True, nullable=False)

    sectors = relationship("SectorModel", back_populates="mountain")


class SectorModel(Base):
    """
    Эта модель отвечает за таблицу с секторами гор
    """

    __tablename__ = "sector"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    lower_level = Column(
        Integer, CheckConstraint("lower_level > 0"), nullable=False
    )
    top_level = Column(
        Integer, CheckConstraint("top_level > lower_level"), nullable=False
    )
    cardinal_point = Column(
        Enum(CardinalPoint, name="cardinal_point_enum"), nullable=False
    )
    mountain_id = Column(Integer, ForeignKey("mountain.id"), nullable=False)

    mountain = relationship("MountainModel", back_populates="sectors")
    facts = relationship("FactModel", back_populates="sector")
    forecasts = relationship("ForecastModel", back_populates="sector")
    monitoring_records = relationship(
        "MonitoringModel", back_populates="sector"
    )


class FactModel(Base):
    """
    Эта модель отвечает за таблицу фактов схода лавины для определенного сектора
    """

    __tablename__ = "fact"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    is_avalanche = Column(Boolean, nullable=False)
    timestamp = Column(DateTime, nullable=False, index=True)
    sector_id = Column(Integer, ForeignKey("sector.id"), nullable=False)

    sector = relationship("SectorModel", back_populates="facts")


class ForecastModel(Base):
    """
    Эта модель отвечает за таблицу прогнозов схода лавины для определенного сектора
    """

    __tablename__ = "forecast"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    forecast_value = Column(Numeric(precision=2, scale=2), nullable=False)
    sector_id = Column(Integer, ForeignKey("sector.id"), nullable=False)

    sector = relationship("SectorModel", back_populates="forecasts")


class MonitoringModel(Base):
    """
    Эта модель отвечает за мониторинг соответствия прогнозов и фактических данных
    """

    __tablename__ = "monitoring"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)
    sector_id = Column(Integer, ForeignKey("sector.id"), nullable=True)

    sector = relationship("SectorModel", back_populates="monitoring_records")
