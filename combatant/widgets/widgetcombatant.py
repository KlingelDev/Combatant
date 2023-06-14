import logging

class CombatantWidget:
    def __init__(self, sm=None):
        self._sm = sm

    def emit(self, signal, *args, **kwargs):
        self._sm.put(signal, *args, **kwargs)
