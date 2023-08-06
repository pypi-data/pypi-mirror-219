from typing import Callable
from typing import Any

from .exceptions import KThreadExecutionTimedOut
from .exceptions import KThreadStartFailed
from .exceptions import KThreadNotAlive

from .utils import terminate_thread

from .classes import KThreadExecutionStatus
from .classes import ResultThread


class KThread:
    def __init__(
        self,
        target: Callable,
        name: str = None,
        daemon: bool = False,
        on_error: Callable | None = None,
    ) -> None:
        self.__target: Callable = target
        self.__thread: ResultThread | None = None
        self.__errhnd: Callable | None = on_error

        self.daemon: bool = daemon
        self.name: str = name

    def start(self, *args: list | tuple, **kwargs: dict) -> None:
        if self.alive:
            raise KThreadStartFailed("Thread is already running")

        self.__thread = ResultThread(
            target=lambda: self.__target(*args, **kwargs),
            daemon=self.daemon,
            name=self.name,
            error_handler=self.__errhnd,
        )
        self.__thread.start()

    def terminate(self, exc: Exception | BaseException = SystemExit) -> None:
        if self.alive:
            terminate_thread(self.__thread, exc)
            self.__thread = None

        else:
            raise KThreadNotAlive("Cannot terminate not running thread")

    def timeout(self, timeout: float, *args: list | tuple, **kwargs: dict) -> Any:
        self.start(*args, **kwargs)
        self.join(timeout=timeout)

        status = self.status

        if not status.done:
            self.terminate()
            raise KThreadExecutionTimedOut(timeout)

        else:
            return status.result

    def join(self, timeout: float | None = None) -> None:
        if self.alive:
            self.__thread.join(timeout)

        else:
            raise KThreadNotAlive("Cannot join not running thread")

    @property
    def alive(self) -> bool:
        if not isinstance(self.__thread, ResultThread):
            return False

        else:
            return self.__thread.is_alive()

    @alive.setter
    def alive(self, _) -> None:
        raise TypeError("Cannot modify the `is_alive` property. It is read-only.")

    @property
    def status(self) -> KThreadExecutionStatus | None:
        return self.__thread.status if isinstance(self.__thread, ResultThread) else None

    @status.setter
    def status(self, _) -> None:
        raise TypeError("Cannot modify the `status` property. It is read-only.")
    
    @property
    def ident(self) -> int:
        if self.alive:
            return self.__thread.ident
        
        else:
            raise KThreadNotAlive("Cannot get not running thread ident")
        
    @ident.setter
    def ident(self, _) -> None:
        raise TypeError("Cannot modify the `ident` property. It is read-only.")

    def __repr__(self) -> str:
        status = "started" if self.alive else "stopped"

        if self.daemon:
            status += " daemon"

        return "{0}({1}, {2})".format(self.__class__.__name__, self.name, status)
