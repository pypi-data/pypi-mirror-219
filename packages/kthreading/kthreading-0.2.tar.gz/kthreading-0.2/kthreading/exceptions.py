class KThreadTerminateFailed(Exception):
    pass

class KThreadStartFailed(Exception):
    pass

class KThreadNotAlive(Exception):
    pass

class KThreadExecutionTimedOut(Exception):
    def __init__(self, timeout: float) -> None:
        self.timeout: float = timeout

    def __str__(self) -> str:
        return "Thread does not end after {0} s.".format(self.timeout)
