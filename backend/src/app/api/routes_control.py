
from fastapi import APIRouter, Depends, HTTPException
from src.app.models import ValveCommand, WateringMode
from src.app.dependencies import get_valve, get_state_repo

router = APIRouter(prefix="/control", tags=["control"])


@router.post("/valve")
def control_valve(
    cmd: ValveCommand,
    valve = Depends(get_valve),
    state_repo = Depends(get_state_repo),
):
    if cmd.action == "open":
        if cmd.seconds and hasattr(valve, "open_for"):
            valve.open_for(cmd.seconds)  # type: ignore[attr-defined]
        else:
            valve.open()
        state_repo.set_valve_open(True)
    elif cmd.action == "close":
        valve.close()
        state_repo.set_valve_open(False)
    else:
        raise HTTPException(status_code=400, detail="Unknown action")
    return {"ok": True}


@router.post("/mode")
def set_mode(
    mode: WateringMode,
    state_repo = Depends(get_state_repo),
):
    if mode.mode not in ("auto", "manual"):
        raise HTTPException(status_code=400, detail="Unknown mode")
    state_repo.set_mode(mode.mode)
    return {"ok": True, "mode": mode.mode}
