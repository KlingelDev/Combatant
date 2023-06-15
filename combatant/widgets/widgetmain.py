import logging
import urwid as u

from .widgetcombatant import *

from .widgetbody import WidgetBody
from .widgetcl import WidgetCL, WidgetCLEdit
from .widgetbody import WidgetBody
from .widgettabs import WidgetTabs, WidgetTabButton

class WidgetMain(CombatantWidgetWrap):
    """
    Houses the frame with tabline, body and command line
    """
    def __init__(self, sm=None):
        self._cmd_key = ':'
        """Set command key"""

        self._tabs = [('time', 'Time', 'T', WidgetTabButton),
                      ('labels', 'Labels', 'L'),
                      ('modify', 'Modify', 'M'),
                      ('summary', 'Summary', 'S'),
                      ('config', 'Config', 'C')]
        """
        Change out Tab/Body classes to implement special behavior
        ```
        0     1      2             3                        4
        name, label, shortcut key, (WidgetTabButton Class), (WidgetCargo Class)
        ```
        """

        self.assemble()
        super(WidgetMain, self).__init__(self._w, sm=sm)

        # u.register_signal(WidgetCLEdit, WidgetCLEdit.signals)
        # u.connect_signal(self, 'CMDMode', self.cmd_mode)
        # u.connect_signal(self._m_cl.edit_line, 'ExitCMDMode', self.cmd_mode)

    def assemble(self):
        """Assemble widget"""
        self._m_tabs = WidgetTabs(tabs=self._tabs, sm=self._sm)
        self._m_body = WidgetBody(tabs=self._tabs, sm=self._sm)
        self._m_cl = WidgetCL(cmd_key=self._cmd_key,
                              cmdm_handler=self.cmd_mode,
                              sm=self._sm)

        self._frame = u.Frame(header = self._m_tabs,
                              body = self._m_body,
                              footer = self._m_cl)

        # self._w = u.AttrWrap(self._frame, 'bg')
        self._w = self._frame

    def app_start(self):
        """Perform at application start"""
        t = self._tabs[0]
        logging.debug(f'AppStart WidgetMain{t!r}')
        self._frame.focus_position = 'header'
        self._m_tabs._bc.focus_position = 1
        self._m_tabs.tbutton_press(self, (t[0], t[1]))

    def keypress(self, size, key):
        if key == 'ctl q' or key == 'ctrl Q':
            u.emit_signal(self, 'Quit')
            return

        if key == self._cmd_key:
            u.emit_signal(self, 'CMDMode', 1)
            return

        # Tab hotkeys
        for t in self._tabs:
            if key == t[2]:
                self._m_tabs.tbutton_press(self, (t[0], t[1]))

        super(WidgetMain, self).keypress(size, key)

    def cmd_mode(self, cmdm):
        """Handle CMD Mode"""
        logging.debug(f'Handle CMDMode {cmdm!r}')
        if cmdm:
            logging.debug('Enter CMDMode')
            self._cmd_mode = True
            self._frame.focus_position = 'footer'
            self._m_cl._wx.focus_position = 1
            self._m_cl.ed_col.focus_position = 1
            self._m_cl.cl_clear()

        else:
            logging.debug('Main Exit CMDMode')
            self._cmd_mode = False
            self._frame.focus_position = 'body'

    def cmd_complete(self):
        pass

    @property
    def body(self):
        return self._m_body

    @property
    def tabs(self):
        return self._m_tabs

    @property
    def cl(self):
        return self._m_cl
