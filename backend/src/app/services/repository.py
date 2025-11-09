
from datetime import datetime
from threading import RLock
from src.app.models import AirReading, SoilReading


class StateRepository:
    def __init__(self) -> None:
        self._lock = RLock()
        self._last_air: AirReading | None = None
        self._last_soil: SoilReading | None = None
        self._valve_open: bool = False
        self._mode: str = "auto"
        self._controller_state: str = "idle"
        self._daily_watered_seconds: int = 0
        self._last_reset_date: datetime | None = None

    def set_air(self, air: AirReading | None) -> None:
        with self._lock:
            self._last_air = air

    def set_soil(self, soil: SoilReading | None) -> None:
        with self._lock:
            self._last_soil = soil

    def set_valve_open(self, is_open: bool) -> None:
        with self._lock:
            self._valve_open = is_open

    def set_mode(self, mode: str) -> None:
        with self._lock:
            self._mode = mode

    def set_controller_state(self, state: str) -> None:
        with self._lock:
            self._controller_state = state

    def add_watered_seconds(self, seconds: int) -> None:
        with self._lock:
            self._daily_watered_seconds += seconds

    def reset_daily_if_needed(self, now: datetime) -> None:
        with self._lock:
            if self._last_reset_date is None or self._last_reset_date.date() != now.date():
                self._last_reset_date = now
                self._daily_watered_seconds = 0

    def snapshot(self) -> dict:
        with self._lock:
            return dict(
                air=self._last_air,
                soil=self._last_soil,
                valve_open=self._valve_open,
                mode=self._mode,
                controller_state=self._controller_state,
                daily_watered_seconds=self._daily_watered_seconds,
            )
