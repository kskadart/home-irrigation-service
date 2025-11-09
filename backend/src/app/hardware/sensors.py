
from datetime import datetime
from abc import ABC, abstractmethod
from random import random
from src.app.models import AirReading, SoilReading


class SensorReaderInterface(ABC):
    @abstractmethod
    def read_air(self) -> AirReading | None:
        ...

    @abstractmethod
    def read_soil(self) -> SoilReading | None:
        ...


class MockSensorReader(SensorReaderInterface):
    """Stub implementation generating somewhat realistic values."""

    def read_air(self) -> AirReading:
        now = datetime.utcnow()
        return AirReading(
            temperature_c=22 + (random() - 0.5) * 2,
            humidity_rel=50 + (random() - 0.5) * 10,
            timestamp=now,
        )

    def read_soil(self) -> SoilReading:
        now = datetime.utcnow()
        return SoilReading(
            temperature_c=18 + (random() - 0.5) * 2,
            moisture_rel=0.35 + (random() - 0.5) * 0.05,
            timestamp=now,
        )
