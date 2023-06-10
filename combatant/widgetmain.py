import logging
import urwid as u

from widgetcl import WidgetCL
from widgetbody import WidgetBody
from widgettabs import WidgetTabs, WidgetTabButton

class WidgetMain(u.WidgetWrap, metaclass = u.signals.MetaSignals):
    signals = ['Quit', 'FocusCL']
    """
    Houses the frame with tabline, body and command line
    """
    def __init__(self):
        self._cmd_key = ':'

        # Change out Tab/Body classes to implement special behavior
        # name, label, shortcut key, (WidgetTabButton Class), (WidgetCargo Class)
        self._tabs = [('time', 'Time', 'T', WidgetTabButton),
                      ('modify', 'Modify', 'M'),
                      ('summary', 'Summary', 'S'),
                      ('config', 'Config', 'C')]

        self.assemble()

        u.connect_signal(self, 'FocusCL', self.focus_cl)

        super(WidgetMain, self).__init__(self._w)

    def assemble(self):
        self._m_tabs = WidgetTabs(tabs=self._tabs)
        self._m_body = WidgetBody(tabs=self._tabs)
        self._m_cl = WidgetCL(cmd_key=self._cmd_key)

        self._frame = u.Frame(header = self._m_tabs,
                              body = self._m_body,
                              footer = self._m_cl)
        self._w = u.AttrWrap(self._frame, 'bg')

    def app_start(self):
        logging.debug('AppStart WidgetMain')

    def keypress(self, size, key):
        logging.debug('Keypress {0}'.format(repr(key)))
        if key == 'ctl q' or key == 'ctrl Q':
            u.emit_signal(self, 'Quit')
            return

        elif key == self._cmd_key:
            self._emit('FocusCL')
            return

        elif key == 'esc':
            self._frame.set_focus('body')
            return

        # Tab hotkeys
        for t in self._tabs:
            if key == t[2]:
                self._m_tabs.tbutton_press(self, (t[0], t[1]))

        super(WidgetMain, self).keypress(size, key)

    def focus_cl(self, d):
        self._frame.focus_position = 'footer'
        self._m_cl._wx.focus_position = 1
        self._m_cl.ed_col.focus_position = 1
        self._m_cl.focus_cl(self)

    @property
    def body(self):
        return self._m_body

    @property
    def tabs(self):
        return self._m_tabs

    @property
    def cl(self):
        return self._m_cl
