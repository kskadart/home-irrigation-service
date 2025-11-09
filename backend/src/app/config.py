
from pydantic import BaseModel, Field


class WateringWindow(BaseModel):
    start_hour: int = 3
    end_hour: int = 6  # not inclusive (3:00–5:59)


class ControllerConfig(BaseModel):
    threshold_low: float = Field(0.38, ge=0.0, le=1.0)
    threshold_high: float = Field(0.45, ge=0.0, le=1.0)
    watering_seconds: int = 90
    soak_minutes: int = 8
    max_cycle_minutes: int = 30
    daily_budget_minutes: int = 20
    window: WateringWindow = WateringWindow()


class AppConfig(BaseModel):
    controller: ControllerConfig = ControllerConfig()
    tick_interval_sec: int = 5


config = AppConfig()
