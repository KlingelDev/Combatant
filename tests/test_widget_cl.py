import logging

import unittest

import urwid as u
from io import StringIO

from combatant.signalmanager import SignalManager
from combatant.signals import CombatantSignals
from combatant.widgets.widgetcl import WidgetCL

logging.basicConfig(filename = 'test.log',
                    encoding = 'utf-8',
                    level = logging.DEBUG)

logger = logging.getLogger()

class WidgetCLTestCase(unittest.TestCase):
    """Test SignalManager"""
    def setUp(self):
        self.sm = SignalManager()
        CombatantSignals.register_signals(sm=self.sm)

        self.cl = WidgetCL(cmd_key=':',
                           cmdm_handler=self.cmdmode,
                           sm=self.sm)
        self.frame=u.Frame(body=u.Filler(u.Text('')),
                           footer=self.cl)

        stdout_buff = StringIO()
        self.ui = u.raw_display.Screen(output=stdout_buff)

        self.uloop = u.MainLoop(self.frame,
                                screen = self.ui,
                                handle_mouse = True,
                                pop_ups = True)

    def tearDown(self):
        pass

    def raise_exit(self, *args):
        raise u.ExitMainLoop

    def cmdmode(self):
        pass

    def test_run(self):
        self.uloop.set_alarm_in(0.1, self.raise_exit)
        self.uloop.run()

