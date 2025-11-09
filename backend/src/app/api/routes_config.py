from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.database.engine import get_session
from src.app.database.repository import ThresholdRepository


router = APIRouter(prefix="/config", tags=["config"])


class ThresholdResponse(BaseModel):
    """Schema for threshold configuration response."""
    id: int
    soil_moisture_low: float
    soil_moisture_high: float
    air_temp_min: float | None
    air_temp_max: float | None
    air_humidity_min: float | None
    air_humidity_max: float | None
    watering_seconds: int
    soak_minutes: int
    daily_budget_minutes: int
    window_start_hour: int
    window_end_hour: int
    
    class Config:
        from_attributes = True


class ThresholdUpdate(BaseModel):
    """Schema for updating threshold configuration."""
    soil_moisture_low: float | None = Field(None, ge=0.0, le=1.0)
    soil_moisture_high: float | None = Field(None, ge=0.0, le=1.0)
    air_temp_min: float | None = None
    air_temp_max: float | None = None
    air_humidity_min: float | None = Field(None, ge=0.0, le=100.0)
    air_humidity_max: float | None = Field(None, ge=0.0, le=100.0)
    watering_seconds: int | None = Field(None, gt=0)
    soak_minutes: int | None = Field(None, gt=0)
    daily_budget_minutes: int | None = Field(None, gt=0)
    window_start_hour: int | None = Field(None, ge=0, lt=24)
    window_end_hour: int | None = Field(None, ge=0, lt=24)


@router.get("/thresholds", response_model=ThresholdResponse)
async def get_thresholds(session: AsyncSession = Depends(get_session)):
    """Get the current threshold configuration."""
    repo = ThresholdRepository(session)
    config = await repo.get_current()
    return config


@router.post("/thresholds", response_model=ThresholdResponse)
async def update_thresholds(
    threshold_data: ThresholdUpdate,
    session: AsyncSession = Depends(get_session),
):
    """Update threshold configuration."""
    repo = ThresholdRepository(session)
    config = await repo.update(
        soil_moisture_low=threshold_data.soil_moisture_low,
        soil_moisture_high=threshold_data.soil_moisture_high,
        air_temp_min=threshold_data.air_temp_min,
        air_temp_max=threshold_data.air_temp_max,
        air_humidity_min=threshold_data.air_humidity_min,
        air_humidity_max=threshold_data.air_humidity_max,
        watering_seconds=threshold_data.watering_seconds,
        soak_minutes=threshold_data.soak_minutes,
        daily_budget_minutes=threshold_data.daily_budget_minutes,
        window_start_hour=threshold_data.window_start_hour,
        window_end_hour=threshold_data.window_end_hour,
    )
    return config

