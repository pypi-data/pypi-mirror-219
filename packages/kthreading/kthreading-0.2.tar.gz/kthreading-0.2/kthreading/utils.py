from ctypes import pythonapi
from ctypes import py_object

from threading import Thread

from .exceptions import KThreadTerminateFailed


def terminate_thread(thread: Thread, exc: Exception) -> bool:
    result = pythonapi.PyThreadState_SetAsyncExc(thread.ident, py_object(exc))

    if result == 0:
        raise KThreadTerminateFailed("Invalid thread ID: {0}".format(thread.ident))

    if result != 1:
        pythonapi.PyThreadState_SetAsyncExc(thread.ident, 0)
        raise KThreadTerminateFailed(
            "Failed to terminate thread with ID {0}".format(thread.ident)
        )

    return True
