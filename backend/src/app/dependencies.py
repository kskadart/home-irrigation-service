
from src.app.hardware.valve import ValveInterface
from src.app.services.controller import WateringController
from src.app.services.repository import StateRepository

_state_repo: StateRepository | None = None
_valve: ValveInterface | None = None
_controller: WateringController | None = None


def set_singletons(
    state_repo: StateRepository,
    valve: ValveInterface,
    controller: WateringController,
) -> None:
    global _state_repo, _valve, _controller
    _state_repo = state_repo
    _valve = valve
    _controller = controller


def get_state_repo() -> StateRepository:
    assert _state_repo is not None
    return _state_repo


def get_valve() -> ValveInterface:
    assert _valve is not None
    return _valve


def get_controller() -> WateringController:
    assert _controller is not None
    return _controller
