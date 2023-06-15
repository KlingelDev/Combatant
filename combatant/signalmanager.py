import logging
import uuid

class SignalConnectError(Exception):
    def __init__(self, signal=''):
        self.message = f"No such signal '{signal}'"
        super(Exception, self).__init__(self.message)

class SignalManager:
    """
    SignalManger
    """
    def __init__(self):
        self.uuid = uuid.uuid4()
        self._que = []
        self._registry = {}

    def register(self, name, desc):
        self._registry[name] = SMSignal(name, desc)

    def connect(self, caller, name, handler):
        if name in self._registry:
            self._registry[name].add_handler(caller, handler)

        else:
            raise SignalConnectError(name)

    def disconnect(self, signal_name, handler=None, caller=None):
        if name in self.registry:
            self._registry[name].remove_handler(handler)

        else:
            raise SignalConnectError(name)

    def process(self):
        """Process signals in the queue"""
       #remove duplicates
        signals = []
        m = self.get()

        while m:
            found = 0
            for s in signals:
                if s[0] == m[0]:
                    found = 1
                    break

            if not found:
                signals.append(m)

            m = self.get()

        for s in signals:
            if s[0] in self._registry:
                for h in self._registry[s[0]].handlers:
                    h[1](*s[1:])

            else:
                raise SignalConnectError(s[0])

    def put(self, signal, *args):
        self._que.append((signal, *args))

    def get(self):
        try:
            return self._que.pop()

        except IndexError:
            return False

class SMSignal:
    def __init__(self, name, desc):
        self._name = name
        self._desc = desc
        self._handlers = []

    def add_handler(self, caller, handler):
        self._handlers.append((caller, handler))

    def remove_handler(self, handler, caller=None):
        for h in self._handlers:
            if caller != None and h[0] == caller:
                self._handlers.remove(h)
                break

            elif caller == None and h[1] == handler:
                self._handlers.remove(h)

    @property
    def name(self) -> str:
        """Return signal name"""
        return self._name

    @property
    def description(self) -> str:
        """Return signal description"""
        return self._desc

    @property
    def handlers(self) -> str:
        """Return signal name"""
        return self._handlers

