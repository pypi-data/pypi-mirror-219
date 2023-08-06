from typing import Callable

from .kthread import KThread


def start_kthread(target: Callable, *args, **kwargs):
    thread = KThread(target=target)
    thread.start(*args, **kwargs)

    return thread
