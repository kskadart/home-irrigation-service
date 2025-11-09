
from datetime import datetime
from app.services.controller import WateringController
from app.services.repository import StateRepository
from app.hardware.valve import MockValve
from app.hardware.sensors import SensorReaderInterface
from app.models import AirReading, SoilReading


class FakeSensors(SensorReaderInterface):
    def __init__(self, moisture: float) -> None:
        self.moisture = moisture

    def read_air(self) -> AirReading | None:
        return None

    def read_soil(self) -> SoilReading | None:
        return SoilReading(
            temperature_c=20.0,
            moisture_rel=self.moisture,
            timestamp=datetime.utcnow(),
        )


def test_controller_opens_valve_when_dry():
    repo = StateRepository()
    valve = MockValve()
    sensors = FakeSensors(moisture=0.2)
    ctrl = WateringController(sensors, valve, repo)
    repo.set_mode("auto")

    ctrl.tick()
    snap = repo.snapshot()
    assert snap["valve_open"] is True


def test_controller_closes_valve_when_wet():
    repo = StateRepository()
    valve = MockValve()
    sensors = FakeSensors(moisture=0.8)
    ctrl = WateringController(sensors, valve, repo)
    repo.set_mode("auto")

    valve.open()
    repo.set_valve_open(True)

    ctrl.tick()
    snap = repo.snapshot()
    assert snap["valve_open"] is False
