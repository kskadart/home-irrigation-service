from datetime import date, time
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.database.engine import get_session
from src.app.database.repository import ScheduleRepository


router = APIRouter(prefix="/schedule", tags=["schedule"])


class ScheduleCreate(BaseModel):
    """Schema for creating a new schedule."""
    name: str = Field(..., min_length=1, max_length=100)
    schedule_date: date
    schedule_time: time
    duration_seconds: int = Field(..., gt=0)
    enabled: bool = True


class ScheduleUpdate(BaseModel):
    """Schema for updating a schedule."""
    name: str | None = Field(None, min_length=1, max_length=100)
    schedule_date: date | None = None
    schedule_time: time | None = None
    duration_seconds: int | None = Field(None, gt=0)
    enabled: bool | None = None


class ScheduleResponse(BaseModel):
    """Schema for schedule response."""
    id: int
    name: str
    schedule_date: date
    schedule_time: time
    duration_seconds: int
    enabled: bool
    
    class Config:
        from_attributes = True


@router.get("/list", response_model=list[ScheduleResponse])
async def list_schedules(session: AsyncSession = Depends(get_session)):
    """List all watering schedules."""
    repo = ScheduleRepository(session)
    schedules = await repo.get_all()
    return schedules


@router.post("/create", response_model=ScheduleResponse, status_code=201)
async def create_schedule(
    schedule_data: ScheduleCreate,
    session: AsyncSession = Depends(get_session),
):
    """Create a new watering schedule."""
    repo = ScheduleRepository(session)
    schedule = await repo.create(
        name=schedule_data.name,
        schedule_date=schedule_data.schedule_date,
        schedule_time=schedule_data.schedule_time,
        duration_seconds=schedule_data.duration_seconds,
        enabled=schedule_data.enabled,
    )
    return schedule


@router.put("/{schedule_id}", response_model=ScheduleResponse)
async def update_schedule(
    schedule_id: int,
    schedule_data: ScheduleUpdate,
    session: AsyncSession = Depends(get_session),
):
    """Update an existing schedule."""
    repo = ScheduleRepository(session)
    schedule = await repo.update(
        schedule_id=schedule_id,
        name=schedule_data.name,
        schedule_date=schedule_data.schedule_date,
        schedule_time=schedule_data.schedule_time,
        duration_seconds=schedule_data.duration_seconds,
        enabled=schedule_data.enabled,
    )
    if schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return schedule


@router.delete("/{schedule_id}")
async def delete_schedule(
    schedule_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Delete a schedule."""
    repo = ScheduleRepository(session)
    deleted = await repo.delete_by_id(schedule_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return {"ok": True, "id": schedule_id}


@router.post("/{schedule_id}/toggle", response_model=ScheduleResponse)
async def toggle_schedule(
    schedule_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Toggle the enabled status of a schedule."""
    repo = ScheduleRepository(session)
    schedule = await repo.toggle_enabled(schedule_id)
    if schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return schedule

