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

        self.waitfortag = None
        self.waitforoccured = False

    def register(self, name, desc):
        self._registry[name] = SMSignal(name, desc)

    def connect(self, caller, name, handler, **kwargs):
        if name in self._registry:
            if len(kwargs):
                self._registry[name].add_handler(caller, handler, kwargs)
            else:
                self._registry[name].add_handler(caller, handler, {})

        else:
            raise SignalConnectError(name)

    def disconnect(self, name, handler=None, caller=None):
        if name in self.registry:
            self._registry[name].remove_handler(handler)

        else:
            raise SignalConnectError(name)

    def setwaitfor(self, tag):
        self.waitfortag = tag

    def process(self):
        """Process signals in the queue"""
        ret = []

        #remove duplicates
        signals = list(set(self._que))
        self._que = []

        #logging.debug('signals {0!r}'.format(signals))
        for s in signals:
            if s[0] in self._registry:
                #logging.debug('signal {0!r}'.format(s[0]))
                if self.waitfortag == s[0]:
                    self.waitforoccured = True
                    logging.debug('Waitfor {0!r} called'.format(self.waitfor))

                for h in self._registry[s[0]].handlers:
                    if len(h[2]):
                       r = h[1].__call__(*s[1:], userdata=h[2])

                    else:
                       #logging.debug('h w/ ud {0!r} {1!r}'.format(h[1], s[1:]))
                       r = h[1].__call__(*s[1:])

                    try:
                        # Calls done. Let caller know
                        if hasattr(h[0], 'callback'):
                            c = getattr(h[0], 'callback')
                            if c: c(r)

                    except AttributeError:
                        raise
            else:
                raise SignalConnectError(s[0])

    def put(self, signal, *args):
        #logging.debug('Put {0!r}'.format(signal))
        self._que.append((signal, *args))

    @property
    def waitfor(self) -> bool:
        """Waitfor handler was seen"""
        return self.waitforoccured

class SMSignal:
    def __init__(self, name, desc):
        self._name = name
        self._desc = desc
        self._handlers = []

    def add_handler(self, caller, handler, kwargs):
        self._handlers.append((caller, handler, kwargs))

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
    def handlers(self) -> list:
        """Return signal name"""
        return self._handlers
