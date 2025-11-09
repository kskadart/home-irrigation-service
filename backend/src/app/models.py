
from datetime import datetime
from pydantic import BaseModel


class AirReading(BaseModel):
    temperature_c: float
    humidity_rel: float
    timestamp: datetime


class SoilReading(BaseModel):
    temperature_c: float
    moisture_rel: float  # 0..1
    timestamp: datetime


class Metrics(BaseModel):
    air: AirReading | None = None
    soil: SoilReading | None = None
    valve_open: bool
    mode: str           # "auto" / "manual"
    state: str          # controller state


class ValveCommand(BaseModel):
    action: str         # "open" / "close"
    seconds: int | None = None


class WateringMode(BaseModel):
    mode: str           # "auto" / "manual"
