import urwid as u
import math, logging

class WidgetCL(u.WidgetWrap, metaclass = u.signals.MetaSignals):
    signals = ['Quit', 'Dirty', 'CMDMode', 'ExitCMDMode', 'CMD']
    _border_char = u'─'

    def __init__(self, cmd_key=':', cmdm_handler=None):
        self._cmd_key = cmd_key
        self._cmds = []
        self.assemble()

        if cmdm_handler != None:
            u.connect_signal(self, 'CMDMode', cmdm_handler)

        super(WidgetCL, self).__init__(self._w)

    def assemble(self, cl_text='timew command...', cols=80, rows=45):
        self.edit_line = WidgetCLEdit(caption='', wrap='clip')
        self.edit_line.set_edit_text(cl_text)

        self._cl_button = WidgetCLButton(cmd_label = self._cmd_key,
                                         on_press = self.focus_cl)
        clb_w = self._cl_button.width
        label = ''
        padding_size = round(cols-clb_w-1)
        logging.debug('clbw %s padding %s' % (clb_w, padding_size))
        border = self._border_char * padding_size
        cursor_position = len(border) + padding_size

        self._top = u'─' + border
        self._bottom = u'─' + border

        self.ed_col = u.Columns([(1, u.Text(' ')),
                      u.Padding(self.edit_line, width=('relative', 100)) ])
        self._cl_box = [
                u.Text(self._top[:-1]),
                self.ed_col,
            u.Text(self._bottom[:-1])
        ]

        self._wx = u.Columns([
            (clb_w, self._cl_button),
            (padding_size, u.Pile(self._cl_box)),
            (1, u.Pile([u.Text(u'┐'),
                        u.Text(u'│'),
                        u.Text(u'┘') ]))
        ])

        self._w = u.AttrMap(self._wx, '', 'highlight')

    def send_cmd(self):
        cmd = self.edit_line.get_edit_text()
        self._cmds.append(cmd)
        u.emit_signal(self, 'CMD', cmd)
        self.cl_clear()

    def cl_clear(self):
        logging.debug('CL Clear')
        self.edit_line.clear()
        u.emit_signal(self, 'Dirty')

    def focus_cl(self, d):
        u.emit_signal(self, 'CMDMode')

    def win_change(self, colrows):
        cols, rows = colrows
        t = self.edit_line.get_edit_text()
        self.assemble(cl_text=t, cols=cols, rows=rows)

class WidgetCLButton(u.Button):
    signals = ['click', 'CMDMode']

    _border_char = u'─'

    def __init__(self, cmd_label=':', on_press=None, user_data=None):
        self._cmd_label = cmd_label
        self.assemble()

        if on_press:
            u.connect_signal(self, 'click', on_press, user_data)

    def assemble(self):
        self._label = u.SelectableIcon("", 0)

        padding_size = 2
        border = self._border_char * (len(self._cmd_label) + padding_size * 2)
        cursor_position = len(border) + padding_size

        self.top    = f'┌{border}┬\n'
        self.middle =  '│{s}{0}{s}│\n'.format(self._cmd_label, s=padding_size* ' ')
        self.bottom = f'└{border}┴'

        self._w = u.Pile([
            u.Text(self.top[:-1]),
            u.Text(self.middle[:-1]),
            u.Text(self.bottom),
        ])

        self._w = u.AttrMap(self._w, '', 'highlight')

    @property
    def width(self):
        return len(self.top)-1

class WidgetCLEdit(u.Edit):
    def clear(self):
        self.set_edit_text('')
        self._invalidate()
