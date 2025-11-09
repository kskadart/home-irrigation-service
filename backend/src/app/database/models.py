from datetime import datetime
from sqlalchemy import Boolean, DateTime, Float, Integer, String, Time, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class WateringSchedule(Base):
    """Calendar-based watering schedule entries."""
    
    __tablename__ = "watering_schedules"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    schedule_date: Mapped[datetime] = mapped_column(Date, nullable=False)
    schedule_time: Mapped[datetime] = mapped_column(Time, nullable=False)
    duration_seconds: Mapped[int] = mapped_column(Integer, nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ThresholdConfig(Base):
    """Dynamic threshold configuration for watering automation."""
    
    __tablename__ = "threshold_configs"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    soil_moisture_low: Mapped[float] = mapped_column(Float, nullable=False, default=0.38)
    soil_moisture_high: Mapped[float] = mapped_column(Float, nullable=False, default=0.45)
    air_temp_min: Mapped[float] = mapped_column(Float, nullable=True)
    air_temp_max: Mapped[float] = mapped_column(Float, nullable=True)
    air_humidity_min: Mapped[float] = mapped_column(Float, nullable=True)
    air_humidity_max: Mapped[float] = mapped_column(Float, nullable=True)
    watering_seconds: Mapped[int] = mapped_column(Integer, nullable=False, default=90)
    soak_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=8)
    daily_budget_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=20)
    window_start_hour: Mapped[int] = mapped_column(Integer, nullable=False, default=3)
    window_end_hour: Mapped[int] = mapped_column(Integer, nullable=False, default=6)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SensorReading(Base):
    """Historical sensor readings for analytics and graphing."""
    
    __tablename__ = "sensor_readings"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    reading_type: Mapped[str] = mapped_column(String(20), nullable=False)
    temperature_c: Mapped[float] = mapped_column(Float, nullable=True)
    humidity_rel: Mapped[float] = mapped_column(Float, nullable=True)
    moisture_rel: Mapped[float] = mapped_column(Float, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)

