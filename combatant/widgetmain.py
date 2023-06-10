import urwid as u

from widgetcl import WidgetCL
from widgetbody import WidgetBody
from widgettabs import WidgetTabs, WidgetTabButton

class WidgetMain(u.WidgetWrap, metaclass = u.signals.MetaSignals):
    signals = ['Quit']
    """
    Houses the frame with tabline, body and command line
    """
    def __init__(self):
        # name, label, (WidgetTabButton Class) for special behavior
        tabs = [('time', 'Time', WidgetTabButton),
                ('modify', 'Modify'),
                ('summary', 'Summary'),
                ('config', 'Config')]

        self.setup(tabs=tabs)

        super(WidgetMain, self).__init__(self._w)

    def setup(self, tabs=[]):
        self._m_tabs = WidgetTabs(tabs=tabs)
        self._m_body = WidgetBody()
        self._m_cl = WidgetCL()

        self._w = u.AttrWrap(u.Frame(header = self._m_tabs,
                                     body = self._m_body,
                                     footer = self._m_cl),
                             'bg')

    def app_start(self):
        pass

    def keypress(self, size, key):
        if key == 'q' or key == 'Q':
            u.emit_signal(self, 'Quit')

        super(WidgetMain, self).keypress(size, key)

    @property
    def body(self):
        return self._m_body

    @property
    def tabs(self):
        return self._m_tabs

    @property
    def cl(self):
        return self._m_cl
