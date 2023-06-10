import urwid as u
import math, logging

class WidgetTabs(u.WidgetWrap, metaclass = u.signals.MetaSignals):
    signals = ['Dirty']

    def __init__(self, tabs=[]):
        self._tabs=tabs
        self.assemble()
        super(WidgetTabs, self).__init__(self._w)

    def assemble(self, cols=80, rows=45):
        self._tab_buttons = []
        for t in self._tabs:
            arg = {'tab_label': t[1],
                   'on_press': self.tbutton_press,
                   'user_data': (t[0], t[1])}
            tb = [t[0], t[2](**arg) if len(t) == 3 else WidgetTabButton(**arg)]
            self._tab_buttons.append(tb)

        bwidth = 0
        bcolumn = []
        for b in self._tab_buttons:
            bwidth += b[1].width
            bcolumn.append((b[1].width, b[1]))

        bcolumn.append(u.Padding(u.Text(u'\n\n'+u'─'*(cols-bwidth))))
        self._w = u.Columns(bcolumn)

    def win_change(self, colrows):
        cols, rows = colrows
        self.assemble(cols=cols, rows=rows)

    def tbutton_press(self, w, data):
        logging.debug('tabpress {0} {1}'.format(repr(k), repr(data)))

class WidgetTabButton(u.Button):
    signals = ['click']

    _border_char = u'─'
    def __init__(self, tab_label='TabLabel', on_press=None, user_data=None):
        self._tab_label = tab_label
        self.assemble()

        super(u.Button, self).__init__(self._w)

        if on_press:
            u.connect_signal(self, 'click', on_press, user_data)

    def assemble(self):
        self._label = u.SelectableIcon("", 0)

        padding_size = 2
        border = self._border_char * (len(self._tab_label) + padding_size * 2)
        cursor_position = len(border) + padding_size

        self.top    = f'┌{border}┐\n'
        self.middle =  '│{s}{0}{s}│\n'.format(self._tab_label, s=padding_size* ' ')
        self.bottom = f'┴{border}┴'

        self._w = u.Pile([
            u.Text(self.top[:-1]),
            u.Text(self.middle[:-1]),
            u.Text(self.bottom),
        ])

        self._w = u.AttrMap(self._w, '', 'highlight')

    @property
    def width(self):
        return len(self.top)-1
