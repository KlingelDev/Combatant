import logging

import unittest

import urwid as u
from io import StringIO

from combatant.signalmanager import SignalManager
from combatant.signals import CombatantSignals
from combatant.widgets.widgetcl import WidgetCL, WidgetCLEdit

logging.basicConfig(filename = 'test.log',
                    encoding = 'utf-8',
                    level = logging.DEBUG)

logger = logging.getLogger()

class WidgetCLTestCase(unittest.TestCase):
    """Test CL Widget"""
    def setUp(self):
        self.sm = SignalManager()
        CombatantSignals.register_signals(sm=self.sm)

        self.cl = WidgetCL(cmd_key=':',
                           cmdm_handler=self.cmdmode,
                           sm=self.sm)
        self.frame=u.Frame(body=u.Filler(u.Text('')),
                           footer=self.cl)

        stdout_buff = StringIO()
        self.scr = u.raw_display.Screen(output=stdout_buff)
        self.uloop = u.MainLoop(self.frame,
                                screen = self.scr,
                                handle_mouse = True,
                                pop_ups = True)

    def tearDown(self):
        pass

    def cmdmode(self):
        pass

    def test_clear(self):
        self.cl.edit_line._edit.set_edit_text('XXX')
        self.cl.cl_clear()
        assert self.cl.edit_line._edit.get_edit_text() == ''

    def test_focus_cl(self):
        self.cl.focus_cl(0)
        f = False
        for s in self.sm._que:
            if s[0] == 'CMDMode':
                f = True
                break

        assert f

class WidgetCLEditTestCase(unittest.TestCase):
    """Test CL Edit Widget"""
    def setUp(self):
        self.sm = SignalManager()
        CombatantSignals.register_signals(sm=self.sm)

        self.cle = WidgetCLEdit(sm=self.sm)
        self.frame=u.Frame(body=u.Filler(u.Text('')),
                           footer=u.Padding(self.cle))

        stdout_buff = StringIO()
        self.scr = u.raw_display.Screen(output=stdout_buff)
        self.uloop = u.MainLoop(self.frame,
                                screen = self.scr,
                                handle_mouse = True,
                                pop_ups = True)

    def test_send_cmd(self):
        self.cle._edit.set_edit_text('TEST')
        self.cle.send_cmd()
        f = False
        for s in self.sm._que:
            if s[0] == 'CMD' and s[1] == 'TEST':
                f = True
                break

        assert f

    def test_popup_closed(self):
        assert self.cle.cmp_is_open() == False

    def test_popup_open(self):
        self.cle.open_pop_up()
        assert self.cle.cmp_is_open()

    def test_send_history(self):
        self.cle._edit.set_edit_text('TEST')
        self.cle.send_cmd()
        assert self.cle._cmds[0] == 'TEST'
