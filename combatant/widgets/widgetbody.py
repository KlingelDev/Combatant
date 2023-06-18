import urwid as u
import logging

from .widgetcombatant import *
from activity import Activity

class CargoError(Exception):
    def __init__(self, cargo=''):
        self.message = f"No cargo named '{cargo}'"
        super(Exception, self).__init__(self.message)

class CargoHandleError(Exception):
    def __init__(self, cargoh=''):
        self.message = f"No cargo handle named '{cargoh}'"
        super(Exception, self).__init__(self.message)

class WidgetBody(CombatantWidgetWrap):
    def __init__(self, tabs=[], sm=None):
        self._tabs = tabs
        self.assemble()

        super(WidgetBody, self).__init__(self._w)


    def assemble(self):
        self.cargo = {'EMPTY': WidgetCargo(sm=self._sm)}
        for t in self._tabs:
            arg = {'tablabel': t[1], 'sm': self._sm}
            self.cargo[t[0]] = t[4](**arg) if len(t) == 5 else WidgetCargo(**arg)

        self._w = self.cargo['EMPTY']

    def win_change(self, colrows):
        cols, rows = colrows

    def tab_switch(self, t):
        self._w = self.cargo[t]

    def focus(self):
        self._w.focus()

class WidgetCargo(CombatantWidgetWrap):
    def __init__(self, tablabel='', sm=None):
        self.tl = u.Filler(u.Text(tablabel))
        self._w = u.Pile([self.tl])

        super(WidgetCargo, self).__init__(self._w)

    def focus(self):
        self._w.focus_position = 0

class TimeWidgetCargo(WidgetCargo):
    def __init__(self, tablabel='', sm=None):
        super(TimeWidgetCargo, self).__init__(tablabel=tablabel, sm=sm)

        self.connect_signal(self, 'StartActivity', self.start_activity)
        self.connect_signal(self, 'StopActivity', self.stop_activity)

    def start_activity(self, a):
        logging.debug('start activity {0!r}'.format(a))
        self.status = u.Filler(u.Text(a.status))
        self.started = u.Filler(u.Text(a.started))

        self._w = u.Pile([self.status, self.started])

    def stop_activity(self, a):
        logging.debug('stopped activity {0!r}'.format(a))
        self.status = u.Filler(u.Text(a.status))
        self.started = u.Filler(u.Text(a.started))

        self._w = u.Pile([self.status, self.started])
