
from datetime import datetime, timedelta
from src.app.config import config
from src.app.hardware.sensors import SensorReaderInterface
from src.app.hardware.valve import ValveInterface
from src.app.services.repository import StateRepository


class WateringController:
    """Simple state machine for automatic watering."""

    def __init__(
        self,
        sensors: SensorReaderInterface,
        valve: ValveInterface,
        state_repo: StateRepository,
    ) -> None:
        self.sensors = sensors
        self.valve = valve
        self.state_repo = state_repo
        self._state: str = "idle"
        self._state_until: datetime | None = None
        self._db_thresholds = None
        self._last_threshold_load: datetime | None = None

    @property
    def state(self) -> str:
        return self._state

    async def _load_thresholds(self):
        """Load thresholds from database (cached for 60 seconds)."""
        now = datetime.utcnow()
        if (
            self._db_thresholds is None
            or self._last_threshold_load is None
            or (now - self._last_threshold_load).total_seconds() > 60
        ):
            from src.app.database.engine import get_engine
            from src.app.database.repository import ThresholdRepository
            from sqlalchemy.ext.asyncio import AsyncSession
            
            try:
                engine = get_engine()
                async with AsyncSession(engine) as session:
                    repo = ThresholdRepository(session)
                    self._db_thresholds = await repo.get_current()
                    self._last_threshold_load = now
            except Exception:
                self._db_thresholds = None
        
        return self._db_thresholds

    def _within_window(self, now: datetime, thresholds=None) -> bool:
        """Check if current time is within watering window."""
        if thresholds:
            return thresholds.window_start_hour <= now.hour < thresholds.window_end_hour
        w = config.controller.window
        return w.start_hour <= now.hour < w.end_hour

    async def _check_scheduled_watering(self, now: datetime) -> bool:
        """Check if there's a scheduled watering event for current time."""
        from src.app.database.engine import get_engine
        from src.app.database.repository import ScheduleRepository
        from sqlalchemy.ext.asyncio import AsyncSession
        
        try:
            engine = get_engine()
            async with AsyncSession(engine) as session:
                repo = ScheduleRepository(session)
                schedules = await repo.get_enabled_for_date(now.date())
                
                for schedule in schedules:
                    schedule_hour = schedule.schedule_time.hour
                    schedule_minute = schedule.schedule_time.minute
                    
                    if now.hour == schedule_hour and now.minute == schedule_minute:
                        return True
        except Exception:
            pass
        
        return False

    def tick(self) -> None:
        """Call this periodically from a background loop."""
        import asyncio
        
        now = datetime.utcnow()
        self.state_repo.reset_daily_if_needed(now)

        # read sensors
        air = self.sensors.read_air()
        soil = self.sensors.read_soil()
        if air is not None:
            self.state_repo.set_air(air)
        if soil is not None:
            self.state_repo.set_soil(soil)

        # sync valve state
        self.state_repo.set_valve_open(self.valve.is_open)

        mode = self.state_repo.snapshot()["mode"]
        if mode != "auto":
            self._state = "manual"
            self.state_repo.set_controller_state(self._state)
            return

        # Reset state to idle if switching from manual to auto
        if self._state == "manual":
            self._state = "idle"

        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                asyncio.create_task(self._auto_tick_async(now, soil))
            else:
                loop.run_until_complete(self._auto_tick_async(now, soil))
        except Exception:
            self._auto_tick(now, soil)

    async def _auto_tick_async(self, now: datetime, soil) -> None:
        """Async version of auto tick that uses database."""
        thresholds = await self._load_thresholds()
        scheduled = await self._check_scheduled_watering(now)
        
        if thresholds:
            await self._auto_tick_with_db(now, soil, thresholds, scheduled)
        else:
            self._auto_tick(now, soil)

    def _auto_tick(self, now: datetime, soil) -> None:
        """Fallback auto tick using config file (when DB is unavailable)."""
        cfg = config.controller
        snap = self.state_repo.snapshot()

        daily_budget_sec = cfg.daily_budget_minutes * 60
        if snap["daily_watered_seconds"] >= daily_budget_sec:
            self._state = "budget_exceeded"
            self.valve.close()
            self.state_repo.set_valve_open(False)
            self.state_repo.set_controller_state(self._state)
            return

        if soil is None:
            self._state = "no_soil_data"
            self.valve.close()
            self.state_repo.set_valve_open(False)
            self.state_repo.set_controller_state(self._state)
            return

        moisture = soil.moisture_rel

        if self._state == "idle":
            if moisture < cfg.threshold_low and self._within_window(now):
                self.valve.open()
                self.state_repo.set_valve_open(True)
                self._state = "watering"
                self._state_until = now + timedelta(seconds=cfg.watering_seconds)
                self.state_repo.add_watered_seconds(cfg.watering_seconds)

        elif self._state == "watering":
            if now >= (self._state_until or now):
                self.valve.close()
                self.state_repo.set_valve_open(False)
                self._state = "soak"
                self._state_until = now + timedelta(minutes=cfg.soak_minutes)

        elif self._state == "soak":
            if now >= (self._state_until or now):
                if moisture < cfg.threshold_low:
                    self.valve.open()
                    self.state_repo.set_valve_open(True)
                    self._state = "watering"
                    self._state_until = now + timedelta(seconds=cfg.watering_seconds)
                    self.state_repo.add_watered_seconds(cfg.watering_seconds)
                else:
                    self._state = "idle"

        # stop watering if too wet
        if moisture > cfg.threshold_high:
            self.valve.close()
            self.state_repo.set_valve_open(False)
            self._state = "idle"

        self.state_repo.set_controller_state(self._state)

    async def _auto_tick_with_db(self, now: datetime, soil, thresholds, scheduled: bool) -> None:
        """Auto tick using database thresholds and schedules."""
        snap = self.state_repo.snapshot()

        daily_budget_sec = thresholds.daily_budget_minutes * 60
        if snap["daily_watered_seconds"] >= daily_budget_sec:
            self._state = "budget_exceeded"
            self.valve.close()
            self.state_repo.set_valve_open(False)
            self.state_repo.set_controller_state(self._state)
            return

        if soil is None:
            self._state = "no_soil_data"
            self.valve.close()
            self.state_repo.set_valve_open(False)
            self.state_repo.set_controller_state(self._state)
            return

        moisture = soil.moisture_rel

        if self._state == "idle":
            should_water = (
                (moisture < thresholds.soil_moisture_low and self._within_window(now, thresholds))
                or scheduled
            )
            if should_water:
                self.valve.open()
                self.state_repo.set_valve_open(True)
                self._state = "watering"
                self._state_until = now + timedelta(seconds=thresholds.watering_seconds)
                self.state_repo.add_watered_seconds(thresholds.watering_seconds)

        elif self._state == "watering":
            if now >= (self._state_until or now):
                self.valve.close()
                self.state_repo.set_valve_open(False)
                self._state = "soak"
                self._state_until = now + timedelta(minutes=thresholds.soak_minutes)

        elif self._state == "soak":
            if now >= (self._state_until or now):
                if moisture < thresholds.soil_moisture_low:
                    self.valve.open()
                    self.state_repo.set_valve_open(True)
                    self._state = "watering"
                    self._state_until = now + timedelta(seconds=thresholds.watering_seconds)
                    self.state_repo.add_watered_seconds(thresholds.watering_seconds)
                else:
                    self._state = "idle"

        # stop watering if too wet
        if moisture > thresholds.soil_moisture_high:
            self.valve.close()
            self.state_repo.set_valve_open(False)
            self._state = "idle"

        self.state_repo.set_controller_state(self._state)
