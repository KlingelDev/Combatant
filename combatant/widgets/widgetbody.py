import urwid as u
import logging

from widgets.widgetcombatant import CombatantWidget

class WidgetBody(u.WidgetWrap, CombatantWidget):
    def __init__(self, tabs=[], sm=None):
        CombatantWidget.__init__(self, sm=sm)

        self._tabs = tabs
        self.assemble()

        u.WidgetWrap.__init__(self, self._w)

    def assemble(self):
        self.cargo = {'EMPTY': WidgetCargo()}
        for t in self._tabs:
            arg = {'txt': t[1]}
            self.cargo[t[0]] = t[3](**arg) if len(t) == 5 else WidgetCargo(**arg)

        self._w = self.cargo['EMPTY']

    def win_change(self, colrows):
        cols, rows = colrows

    def tab_switch(self, t):
        self._w = self.cargo[t]

class WidgetCargo(u.WidgetWrap, metaclass = u.signals.MetaSignals):
    signals = ['Dirty']

    def __init__(self, txt=''):
        self._w = u.Filler(u.Text(txt))

        super(WidgetCargo, self).__init__(self._w)
