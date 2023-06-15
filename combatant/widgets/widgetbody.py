import urwid as u
import logging

from .widgetcombatant import *

class WidgetBody(CombatantWidgetWrap):
    def __init__(self, tabs=[], sm=None):
        self._tabs = tabs
        self.assemble()

        super(WidgetBody, self).__init__(self._w)

    def assemble(self):
        self.cargo = {'EMPTY': WidgetCargo(sm=self._sm)}
        for t in self._tabs:
            arg = {'txt': t[1], 'sm': self._sm}
            self.cargo[t[0]] = t[3](**arg) if len(t) == 5 else WidgetCargo(**arg)

        self._w = self.cargo['EMPTY']

    def win_change(self, colrows):
        cols, rows = colrows

    def tab_switch(self, t):
        self._w = self.cargo[t]

class WidgetCargo(CombatantWidgetWrap):
    def __init__(self, txt='', sm=None):
        self._w = u.Filler(u.Text(txt))
        super(WidgetCargo, self).__init__(self._w)
