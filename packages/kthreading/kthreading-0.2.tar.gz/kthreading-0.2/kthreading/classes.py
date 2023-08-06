from typing import Callable
from typing import Any

from threading import Thread

from traceback import format_exc


class KThreadExecutionStatus:
    def __init__(self, done: bool, success: bool | None, result: Any) -> None:
        self.done: bool = done
        self.success: bool | None = success
        self.result: Any = result


class KThreadUncaughtException:
    def __init__(self, instance: Any, name: str, text: str, full_text: str):
        self.instance: Any = instance
        self.name: str = name
        self.text: str = text
        self.full_text: str = full_text


class ResultThread(Thread):
    def __init__(
        self,
        target: Callable,
        daemon: bool,
        name: str,
        error_handler: Callable | None = None,
    ) -> None:
        self.target: Callable = target
        self.error_handler: Callable | None = error_handler
        self.status = KThreadExecutionStatus(False, None, None)

        def executor():
            try:
                self.status = KThreadExecutionStatus(True, True, self.target())

            except Exception as exc:
                if self.error_handler:
                    instance = type(exc)
                    name = type(exc).__name__
                    text = str(exc)
                    full_text = format_exc()

                    exc_class = KThreadUncaughtException(
                        instance, name, text, full_text
                    )

                    self.status = KThreadExecutionStatus(True, False, exc_class)
                    self.error_handler(exc_class)

                else:
                    raise exc

        super().__init__(target=executor, daemon=daemon, name=name)
