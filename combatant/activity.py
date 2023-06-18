from datetime import datetime as dt

class Activity:
    def __init__(self, status=None,
                       started=None,
                       current=None,
                       ended=None,
                       total=None,
                       tags=[]):

        self.status = status
        self.started = dt.fromisoformat(started) if started != None else None
        self.current = dt.fromisoformat(current) if current != None else None
        self.ended = dt.fromisoformat(ended) if ended != None else None
        self.total = dt.fromisoformat(total) if total != None else None
        self.tags = []

    def start(self):
        pass

    def stop(self):
        pass
