from datetime import date, time, datetime
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.database.models import WateringSchedule, ThresholdConfig, SensorReading


class ScheduleRepository:
    """Repository for watering schedule CRUD operations."""
    
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
    
    async def create(
        self,
        name: str,
        schedule_date: date,
        schedule_time: time,
        duration_seconds: int,
        enabled: bool = True,
    ) -> WateringSchedule:
        """Create a new watering schedule."""
        schedule = WateringSchedule(
            name=name,
            schedule_date=schedule_date,
            schedule_time=schedule_time,
            duration_seconds=duration_seconds,
            enabled=enabled,
        )
        self.session.add(schedule)
        await self.session.commit()
        await self.session.refresh(schedule)
        return schedule
    
    async def get_by_id(self, schedule_id: int) -> WateringSchedule | None:
        """Get a schedule by ID."""
        result = await self.session.execute(
            select(WateringSchedule).where(WateringSchedule.id == schedule_id)
        )
        return result.scalar_one_or_none()
    
    async def get_all(self) -> list[WateringSchedule]:
        """Get all schedules."""
        result = await self.session.execute(select(WateringSchedule))
        return list(result.scalars().all())
    
    async def get_enabled_for_date(self, target_date: date) -> list[WateringSchedule]:
        """Get enabled schedules for a specific date."""
        result = await self.session.execute(
            select(WateringSchedule).where(
                WateringSchedule.schedule_date == target_date,
                WateringSchedule.enabled == True
            )
        )
        return list(result.scalars().all())
    
    async def update(
        self,
        schedule_id: int,
        name: str | None = None,
        schedule_date: date | None = None,
        schedule_time: time | None = None,
        duration_seconds: int | None = None,
        enabled: bool | None = None,
    ) -> WateringSchedule | None:
        """Update a schedule."""
        schedule = await self.get_by_id(schedule_id)
        if schedule is None:
            return None
        
        if name is not None:
            schedule.name = name
        if schedule_date is not None:
            schedule.schedule_date = schedule_date
        if schedule_time is not None:
            schedule.schedule_time = schedule_time
        if duration_seconds is not None:
            schedule.duration_seconds = duration_seconds
        if enabled is not None:
            schedule.enabled = enabled
        
        schedule.updated_at = datetime.utcnow()
        await self.session.commit()
        await self.session.refresh(schedule)
        return schedule
    
    async def toggle_enabled(self, schedule_id: int) -> WateringSchedule | None:
        """Toggle the enabled status of a schedule."""
        schedule = await self.get_by_id(schedule_id)
        if schedule is None:
            return None
        
        schedule.enabled = not schedule.enabled
        schedule.updated_at = datetime.utcnow()
        await self.session.commit()
        await self.session.refresh(schedule)
        return schedule
    
    async def delete_by_id(self, schedule_id: int) -> bool:
        """Delete a schedule by ID."""
        result = await self.session.execute(
            delete(WateringSchedule).where(WateringSchedule.id == schedule_id)
        )
        await self.session.commit()
        return result.rowcount > 0


class ThresholdRepository:
    """Repository for threshold configuration operations."""
    
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
    
    async def get_current(self) -> ThresholdConfig:
        """Get the current threshold configuration (creates default if none exists)."""
        result = await self.session.execute(
            select(ThresholdConfig).order_by(ThresholdConfig.id.desc()).limit(1)
        )
        config = result.scalar_one_or_none()
        
        if config is None:
            config = ThresholdConfig()
            self.session.add(config)
            await self.session.commit()
            await self.session.refresh(config)
        
        return config
    
    async def update(
        self,
        soil_moisture_low: float | None = None,
        soil_moisture_high: float | None = None,
        air_temp_min: float | None = None,
        air_temp_max: float | None = None,
        air_humidity_min: float | None = None,
        air_humidity_max: float | None = None,
        watering_seconds: int | None = None,
        soak_minutes: int | None = None,
        daily_budget_minutes: int | None = None,
        window_start_hour: int | None = None,
        window_end_hour: int | None = None,
    ) -> ThresholdConfig:
        """Update threshold configuration."""
        config = await self.get_current()
        
        if soil_moisture_low is not None:
            config.soil_moisture_low = soil_moisture_low
        if soil_moisture_high is not None:
            config.soil_moisture_high = soil_moisture_high
        if air_temp_min is not None:
            config.air_temp_min = air_temp_min
        if air_temp_max is not None:
            config.air_temp_max = air_temp_max
        if air_humidity_min is not None:
            config.air_humidity_min = air_humidity_min
        if air_humidity_max is not None:
            config.air_humidity_max = air_humidity_max
        if watering_seconds is not None:
            config.watering_seconds = watering_seconds
        if soak_minutes is not None:
            config.soak_minutes = soak_minutes
        if daily_budget_minutes is not None:
            config.daily_budget_minutes = daily_budget_minutes
        if window_start_hour is not None:
            config.window_start_hour = window_start_hour
        if window_end_hour is not None:
            config.window_end_hour = window_end_hour
        
        config.updated_at = datetime.utcnow()
        await self.session.commit()
        await self.session.refresh(config)
        return config


class SensorReadingRepository:
    """Repository for sensor reading history."""
    
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
    
    async def create(
        self,
        reading_type: str,
        temperature_c: float | None = None,
        humidity_rel: float | None = None,
        moisture_rel: float | None = None,
    ) -> SensorReading:
        """Create a new sensor reading."""
        reading = SensorReading(
            reading_type=reading_type,
            temperature_c=temperature_c,
            humidity_rel=humidity_rel,
            moisture_rel=moisture_rel,
        )
        self.session.add(reading)
        await self.session.commit()
        await self.session.refresh(reading)
        return reading
    
    async def get_recent(self, reading_type: str, limit: int = 100) -> list[SensorReading]:
        """Get recent sensor readings of a specific type."""
        result = await self.session.execute(
            select(SensorReading)
            .where(SensorReading.reading_type == reading_type)
            .order_by(SensorReading.timestamp.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

