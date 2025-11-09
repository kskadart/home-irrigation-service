
import threading
import time
from abc import ABC, abstractmethod


class ValveInterface(ABC):
    @abstractmethod
    def open(self) -> None:
        ...

    @abstractmethod
    def close(self) -> None:
        ...

    @property
    @abstractmethod
    def is_open(self) -> bool:
        ...


class MockValve(ValveInterface):
    """In-memory stub for development and tests."""

    def __init__(self) -> None:
        self._open = False
        self._lock = threading.Lock()

    def open(self) -> None:
        with self._lock:
            self._open = True

    def close(self) -> None:
        with self._lock:
            self._open = False

    @property
    def is_open(self) -> bool:
        with self._lock:
            return self._open


class TimedValveWrapper(ValveInterface):
    """Wrapper that can open valve for a fixed time in a background thread."""

    def __init__(self, inner: ValveInterface) -> None:
        self._inner = inner
        self._timer_thread: threading.Thread | None = None
        self._timer_lock = threading.Lock()

    def open(self) -> None:
        self._inner.open()

    def close(self) -> None:
        self._inner.close()

    @property
    def is_open(self) -> bool:
        return self._inner.is_open

    def open_for(self, seconds: int) -> None:
        self.open()

        def worker() -> None:
            time.sleep(seconds)
            self.close()

        with self._timer_lock:
            if self._timer_thread and self._timer_thread.is_alive():
                # do not cancel previous, just start another
                pass
            self._timer_thread = threading.Thread(target=worker, daemon=True)
            self._timer_thread.start()
