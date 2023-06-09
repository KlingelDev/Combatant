import urwid as u
import logging

class WidgetTabs(u.WidgetWrap, metaclass = u.signals.MetaSignals):
    signals = ['Dirty']

    def __init__(self):
        self.assemble()
        super(WidgetTabs, self).__init__(self._w)

    def assemble(self):
        self.time_button = WidgetTabButton(u' Time ', on_press=None)
        self.modify_button = WidgetTabButton(u'Modify', on_press=None)
        self.summary_button = WidgetTabButton(u'Summary', on_press=None)
        self.config_button = WidgetTabButton(u'Config', on_press=None)

        self._w = u.Columns([(48, u.GridFlow([
            self.time_button,
            self.modify_button,
            self.summary_button,
            self.config_button
        ], cell_width=12, h_sep=0, v_sep=0, align="left")),
          (74,  u.Padding(u.Text(u'\n\n'+u'─'*20),
                          align = 'left',
                          width = 'pack',
                          right=0,
                          left=-80)
           )
        ], dividechars=0)

    def win_change(self, colrows):
        cols, rows = colrows

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

        self.top = u'┌' + border + u'┬\n'
        self.middle = u'│  ' + self._tab_label + u'  │\n'
        #self.bottom = u'└' + border + u'┴'
        self.bottom = u'┴' + border + u'┴'

        self._w = u.Pile([
            u.Text(self.top[:-1]),
            u.Text(self.middle[:-1]),
            u.Text(self.bottom),
        ])

        self._w = u.AttrMap(self._w, '', 'highlight')
