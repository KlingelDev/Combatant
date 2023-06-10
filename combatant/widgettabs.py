import urwid as u
import math, logging

class WidgetTabs(u.WidgetWrap, metaclass = u.signals.MetaSignals):
    signals = ['Dirty']

    def __init__(self):
        self.assemble()
        super(WidgetTabs, self).__init__(self._w)

    def assemble(self, cols=80, rows=45):
        self._tab_buttons = [
            ['time_button', WidgetTabButton(u' Time ', on_press=None)],
            ['modify_button', WidgetTabButton(u'Modify', on_press=None)],
            ['summary_button', WidgetTabButton(u'Summary', on_press=None)],
            ['config_button', WidgetTabButton(u'Config', on_press=None)]
        ]

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

class WidgetTabButton(u.Button):
    signals = ['click']

    _border_char = u'─'
    def __init__(self, tab_label=':', on_press=None, user_data=None):
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

        logging.debug('tab {0} bz {1}'.format(self._tab_label,
                                              len(border)))

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
