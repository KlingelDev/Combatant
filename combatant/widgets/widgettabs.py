import urwid as u
import math, logging

class WidgetTabs(u.WidgetWrap, metaclass = u.signals.MetaSignals):
    signals = ['Dirty', 'TabSwitch']

    def __init__(self, tabs=[]):
        self._tabs=tabs
        self.assemble()
        super(WidgetTabs, self).__init__(self._w)

    def assemble(self, cols=80, rows=45):
        self._tab_buttons = []
        for t in self._tabs:
            # Make button WidgetTabButton or sth more special
            arg = {'tab_label': t[1],
                   'on_press': self.tbutton_press,
                   'user_data': (t[0], t[1])}

            tbm = t[3](**arg) if len(t) == 4 else WidgetTabButton(**arg)
            tb = [t[0], tbm, u.AttrMap(tbm, '')]

            self._tab_buttons.append(tb)

        bwidth = 0
        bspace = u.Text(' ')
        bcolumn = []
        for b in self._tab_buttons:
            if b[0] == 'config':
                bcolumn.append(bspace)

            bwidth += b[1].width
            bcolumn.append((b[1].width, b[2]))

        bcolumn[-2] = u.Text(' '*(cols-bwidth))
        self._bc =u.Columns(bcolumn)
        tabborder = u.AttrMap(u.Text('▔'*(cols)),'tabborder')
        self._w = u.GridFlow([
            self._bc,
            tabborder
            ], cell_width=cols, h_sep=0, v_sep=0, align='left')

    def win_change(self, colrows):
        cols, rows = colrows
        self.assemble(cols=cols, rows=rows)

    def tbutton_press(self, w, data):
        pt = data[0]
        logging.debug('tabl {0}'.format(pt))
        for t in self._tab_buttons:
            if pt == t[0]:
                logging.debug('t2 {0}'.format(repr(t[2].get_attr_map())))
                t[2].set_attr_map({'tabnormal': 'tabselected'})
            else:
                t[2].set_attr_map({'tabselected': 'tabnormal'})

        u.emit_signal(self, 'TabSwitch', pt)
        logging.debug('tabpress {0} {1}'.format(repr(w), repr(data)))

class WidgetTabButton(u.Button):
    signals = ['click']

    def __init__(self, tab_label='TabLabel', on_press=None, user_data=None):
        self._tab_label = tab_label
        self.assemble()

        super(u.Button, self).__init__(self._w)

        if on_press:
            u.connect_signal(self, 'click', on_press, user_data)

    def assemble(self):
        self._label = u.SelectableIcon("", 0)

        padding_size = 2
        # border = self._border_char * (len(self._tab_label) + padding_size * 2)
        # cursor_position = len(border) + padding_size

        self.middle =  '{s}{0}{s}'.format(self._tab_label, s=padding_size* ' ')

        self._w = u.Pile([
            u.AttrMap(u.Text(self.middle, wrap='clip'), 'tabnormal', 'tabselected')
        ])

        self._w = u.AttrMap(self._w , 'tabnormal', 'tabselected')

    @property
    def width(self):
        return len(self.middle)
