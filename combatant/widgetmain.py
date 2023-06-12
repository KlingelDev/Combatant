import logging
import urwid as u

from widgetcl import WidgetCL
from widgetbody import WidgetBody
from widgettabs import WidgetTabs, WidgetTabButton

class WidgetMain(u.WidgetWrap, metaclass = u.signals.MetaSignals):
    signals = ['Quit', 'FocusCL', 'CMDMode', 'ExitCMDMode']
    """
    Houses the frame with tabline, body and command line
    """
    def __init__(self):
        self._cmd_key = ':'
        self._cmd_mode = False

        # Change out Tab/Body classes to implement special behavior
        # name, label, shortcut key, (WidgetTabButton Class), (WidgetCargo Class)
        self._tabs = [('time', 'Time', 'T', WidgetTabButton),
                      ('labels', 'Labels', 'L'),
                      ('modify', 'Modify', 'M'),
                      ('summary', 'Summary', 'S'),
                      ('config', 'Config', 'C')]

        self.assemble()

        u.connect_signal(self, 'CMDMode', self.cmd_mode)
        u.connect_signal(self, 'ExitCMDMode', self.exit_cmd_mode)

        super(WidgetMain, self).__init__(self._w)

    def assemble(self):
        self._m_tabs = WidgetTabs(tabs=self._tabs)
        self._m_body = WidgetBody(tabs=self._tabs)
        self._m_cl = WidgetCL(cmd_key=self._cmd_key, cmdm_handler=self.cmd_mode)

        self._frame = u.Frame(header = self._m_tabs,
                              body = self._m_body,
                              footer = self._m_cl)
        self._w = u.AttrWrap(self._frame, 'bg')

    def app_start(self):
        t = self._tabs[0]
        logging.debug(f'AppStart WidgetMain{t!r}')
        self._frame.focus_position = 'header'
        self._m_tabs._bc.focus_position = 1
        self._m_tabs.tbutton_press(self, (t[0], t[1]))

    def keypress(self, size, key):
        if key == 'ctl q' or key == 'ctrl Q':
            u.emit_signal(self, 'Quit')
            return

        if not self._cmd_mode:
            if key == self._cmd_key:
                self._cmd_mode = True
                u.emit_signal(self, 'CMDMode')
                return

        if self._cmd_mode:
            if key == 'enter':
                logging.debug('Send CMD')
                self._m_cl.send_cmd()
                return

            if key == 'esc':
                logging.debug('Exit CMDMode')
                self._frame.set_focus('body')
                self._cmd_mode = False
                return

        # Tab hotkeys
        for t in self._tabs:
            if key == t[2]:
                self._m_tabs.tbutton_press(self, (t[0], t[1]))

        super(WidgetMain, self).keypress(size, key)

    def cmd_mode(self):
        logging.debug('Enter CMDMode')
        self._cmd_mode = True
        self._frame.focus_position = 'footer'
        self._m_cl._wx.focus_position = 1
        self._m_cl.ed_col.focus_position = 1
        self._m_cl.cl_clear()

    def exit_cmd_mode(self):
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
