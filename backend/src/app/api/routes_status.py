
from fastapi import APIRouter, Depends
from src.app.models import Metrics
from src.app.dependencies import get_state_repo, get_controller, get_valve

router = APIRouter(prefix="/status", tags=["status"])


@router.get("/metrics", response_model=Metrics)
def get_metrics(
    state_repo = Depends(get_state_repo),
    controller = Depends(get_controller),
    valve = Depends(get_valve),
):
    snap = state_repo.snapshot()
    return Metrics(
        air=snap["air"],
        soil=snap["soil"],
        valve_open=snap["valve_open"],
        mode=snap["mode"],
        state=snap["controller_state"],
    )
