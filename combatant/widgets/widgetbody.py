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

    def focus(self):
        self._w.focus()

class WidgetCargo(CombatantWidgetWrap):
    def __init__(self, txt='', sm=None):
        self.txt = u.Filler(u.Text(txt))
        self._w = u.Pile([self.txt])
        super(WidgetCargo, self).__init__(self._w)

    def focus(self):
        self._w.focus_position = 0

