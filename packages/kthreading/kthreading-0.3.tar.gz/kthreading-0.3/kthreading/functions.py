from typing import Callable

from time import sleep

from .kthread import KThread


def start_kthread(target: Callable, daemon: bool = False, *args, **kwargs):
    thread = KThread(target=target, daemon=daemon)
    thread.start(*args, **kwargs)

    return thread
