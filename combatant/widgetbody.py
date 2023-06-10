import urwid as u
import logging

class WidgetBody(u.WidgetWrap, metaclass = u.signals.MetaSignals):
    signals = ['Quit', 'Dirty']

    def __init__(self, tabs=[]):
        self._tabs = tabs
        self.setup()

        super(WidgetBody, self).__init__(self._w)

    def setup(self):
        self.cargo = {}
        for t in self._tabs:
            self.cargo[t[0]] = WidgetCargo(t[1])

        # Set 'random' cargo for now, till AppStart
        self._w = self.cargo[list(self.cargo.keys())[0]]

    def win_change(self, colrows):
        cols, rows = colrows

    def app_start(self):
        pass

    def tab_switch(self, t):
        self._w = self.cargo[t]
        u.emit_signal(self, 'Dirty')

class WidgetCargo(u.WidgetWrap, metaclass = u.signals.MetaSignals):
    signals = ['Dirty']

    def __init__(self, txt):
        self._w = u.Filler(u.Text(txt))

        super(WidgetCargo, self).__init__(self._w)
