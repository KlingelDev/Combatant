from datetime import datetime as dt

class Activity:
    def __init__(self, status=None,
                       started=None,
                       current=None,
                       ended=None,
                       total=None,
                       tags=[]):

        self._status = status
        self._started = dt.fromisoformat(started) if started != None else None
        self._current = dt.fromisoformat(current) if current != None else None
        self._ended = dt.fromisoformat(ended) if ended != None else None
        self._total = dt.fromisoformat(total) if total != None else None
        self._tags = []

    def start(self):
        pass

    def stop(self):
        pass


    @property
    def status(self) -> str:
        """Return status"""
        return self._status

    @status.setter
    def status(self, s):
        """Set status"""
        self._status = s

    @property
    def started(self) -> str:
        """Return started date"""
        if self._started:
            return self._started.isoformat()

        return None

    @property
    def current(self) -> str:
        """Return time running"""
        if self._current:
            return self._current.isoformat()

        return None

    @property
    def ended(self) -> str:
        """Return time ended"""
        if self._ended:
            return self._ended.isoformat()

        return None

    @property
    def total(self) -> str:
        """Return time running total"""
        if self._total:
            return self._total.isoformat()

        return None
