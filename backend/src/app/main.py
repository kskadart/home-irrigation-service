
import threading
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.app.config import config
from src.app.hardware.sensors import MockSensorReader, SensorReaderInterface
from src.app.hardware.valve import MockValve, TimedValveWrapper, ValveInterface
from src.app.services.repository import StateRepository
from src.app.services.controller import WateringController
from src.app.api import routes_status, routes_control, routes_schedule, routes_config
from src.app import dependencies
from src.app.database.engine import init_db, create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    init_db()
    await create_tables()
    yield


app = FastAPI(title="Irrigation Controller", lifespan=lifespan)

# Add CORS middleware to allow browser requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# singletons
_state_repo = StateRepository()
_sensors: SensorReaderInterface = MockSensorReader()
_valve_inner: ValveInterface = MockValve()
_valve = TimedValveWrapper(_valve_inner)
_controller = WateringController(_sensors, _valve, _state_repo)

# expose for DI
dependencies.set_singletons(_state_repo, _valve, _controller)


def _background_loop() -> None:
    while True:
        _controller.tick()
        time.sleep(config.tick_interval_sec)


_thread = threading.Thread(target=_background_loop, daemon=True)
_thread.start()

# routers
app.include_router(routes_status.router)
app.include_router(routes_control.router)
app.include_router(routes_schedule.router)
app.include_router(routes_config.router)


# to run: uvicorn app.main:app --host 0.0.0.0 --port 8000
