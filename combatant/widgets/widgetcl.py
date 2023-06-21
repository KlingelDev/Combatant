import urwid as u
import math, logging, regex

from typing import Literal

from .widgetcombatant import *

from twcommand import TimeWCommand

class WidgetCL(CombatantWidgetWrap):
    _selectable = True
    """
    Command line widget containing commandline button and text edit
    """
    _border_char = u'─'

    def __init__(self, cmd_key=':', cmdm_handler=None, sm=None):
        self._cmd_key = cmd_key
        self.assemble()

        super(WidgetCL, self).__init__(self._w)

        if cmdm_handler != None:
            self.connect_signal(self.edit_line, 'CMDMode', cmdm_handler)
            self.connect_signal(self._cl_button, 'CMDMode', cmdm_handler)

    def assemble(self, cl_text='timew command...', cols=80, rows=45):
        self.edit_line = WidgetCLEdit(caption='', wrap='clip', sm=self._sm)
        self.edit_line.set_edit_text(cl_text)

        self._cl_button = WidgetCLButton(cmd_label = self._cmd_key,
                                         on_press = self.focus_cl,
                                         sm=self._sm)
        clb_w = self._cl_button.width
        label = ''
        padding_size = round(cols-clb_w-1)
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

    def cl_clear(self):
        logging.debug('CL Clear')
        self.edit_line.clear()

    def focus_cl(self, d):
        self.emit('CMDMode', True)

    def win_change(self, colrows):
        cols, rows = colrows
        t = self.edit_line.get_edit_text()
        self.assemble(cl_text=t, cols=cols, rows=rows)

class WidgetCLEdit(CombatantPopUpLauncher):
    """
        WidgetCLEdit
        AutoCmp - Credits jakun stackoverflow.com/questions/58319414
    """
    ucommand_map = u.CommandMap()

    def __init__(self, caption='', wrap='clip', sm=None):
        self._cmd_mode = False
        self._cmds = []
        """Command history"""

        self.cmp_pos = 0
        """Position in CLEdit"""

        self.cmp_length = 20
        """Autocomplete popup width"""

        self._edit = u.Edit()
        self._w = u.AttrWrap(self._edit, 'cl')

        super(WidgetCLEdit, self).__init__(self._w)

    def keypress(self, size, key):
        """
        Open autocompletion popup and let it handle keypress via
        `catch_keypress`.
        """
        logging.debug(f"CLEdit keypress '{key}'")
        # if key == 'esc':
        #     if self.cmp_is_open():
        #         self.close_pop_up()
        #     else:
        #         self.emit('CMDMode', False)
        #     return
        if self._edit.valid_char(key):
            if not self.cmp_is_open():
                self.open_pop_up()
            return

        elif key == 'enter' and not self.cmp_is_open():
            logging.debug('Send CMD')
            self._cmd_mode = True
            self.send_cmd()
            return

        super(WidgetCLEdit, self).keypress(size, key)

    def catch_keypress(self, key):
        """
        Catches keypresses of autocompletion popup.
        TODO: ctrl-c ctrl-v, select text
        """
        logging.debug(f"CLEdit catch_keypress '{key}'")

        cmd = self._command_map[key]
        #if self._edit.valid_char(key):

        if cmd == u.CURSOR_LEFT:
            p = self._w.edit_pos
            if p == 0:
                return key
            p = u.move_prev_char(self._w.edit_text, 0, p)
            self._w.set_edit_pos(p)

        elif cmd == u.CURSOR_RIGHT:
            p = self._w.edit_pos
            if p >= len(self._w.edit_text):
                return key
            p = u.move_next_char(self._w.edit_text, p,
                                 len(self._w.edit_text))
            self._w.set_edit_pos(p)

        elif cmd == u.CURSOR_UP:
            self._pop_up_widget.select(-1)

        elif cmd == u.CURSOR_DOWN:
            self._pop_up_widget.select(1)

        elif key == "tab":
            self._pop_up_widget.select(1)

        elif key == "shift tab":
            self._pop_up_widget.select(-1)

        elif key == "backspace":
            if not self._w._delete_highlighted():
                p = self._w.edit_pos
                if p == 0:
                    return key

                p = u.move_prev_char(self._w.edit_text,0,p)

                et = self._w.edit_text
                ep = self._w.edit_pos

                self._w.set_edit_text(et[:p] + et[ep:])
                self._w.set_edit_pos(p)

            self.update_autocmp()

        elif key == "delete":
            self._w.pref_col_maxcol = None, None
            if not self._w._delete_highlighted():
                p = self._w.edit_pos
                if p >= len(self._w.edit_text):
                    return key

                et = self._w.edit_text
                ep = self._w.edit_pos

                p = u.move_next_char(et, p, len(et))

                self._w.set_edit_text(et[:ep] + et[p:])

            self.update_autocmp()

        elif key == "home":
            self._w.set_edit_pos(0)

        elif key == "end":
            self._w.set_edit_pos(len(self._w.edit_text))

        elif key == 'esc':
            logging.debug('Send ExitCMDMode False')
            if self.cmp_is_open():
                self._pop_up_widget.unselect()
                self.close_pop_up()
            else:
                self._pop_up_widget.unselect()
                self.emit('CMDMode', False)
            return

        elif key == 'enter':
            if self.cmp_is_open():
                # replace half command with one selected in cmp list
                if self._pop_up_widget.select:
                    et = self._w.edit_text
                    s = self._pop_up_widget.get_selected()

                    et = regex.sub('(\w+)[\s]*$', s, et)
                    et += ' '
                    self._w.set_edit_text(et)
                    self._w.set_edit_pos(len(et))

                    self._pop_up_widget.unselect()
                    self.close_pop_up()
                return

            else:
                logging.debug('Send CMD')
                self._cmd_mode = True
                self.send_cmd()
                return
        else:
            """Pass non-command chars to Edit, update autocompletion"""
            self._edit.insert_text(key)

            if not self.cmp_is_open():
                self.open_pop_up()

            # Update autocompletion
            self.update_autocmp()

        return key

    def send_cmd(self):
        cmd = self.get_edit_text()
        self._cmds.append(cmd)
        self.emit('CMD', cmd)
        self.clear()

    def cmp_is_open(self):
        return self._pop_up_widget != None

    def render(self, size, focus=False):
        if self.cmp_is_open():
            focus = True

        return super(WidgetCLEdit, self).render(size, focus)

    def create_pop_up(self):
        return CMPPopUp(self.catch_keypress)

    def get_pop_up_parameters(self):
        #height = len(TimeWCommand.supported_commands)
        #width = max(len(x) for x in CLCommands.supported)
        l = len(self._pop_up_widget._body)
        l = len(self._pop_up_widget._body)
        l = 1 if l == 0 else l

        return {'left': self.cmp_pos,
                'top': -(l),
                'overlay_width': self.cmp_length,
                'overlay_height': l
               }

    def update_autocmp(self):
        """
        get CL input, update autocomplete popup
        """
        # Get strlength for window size
        cmpl = 0
        self.cmp_pos = 0

        ep = self._w.edit_pos
        et = self._w.edit_text

        # Remove completed commands/show args
        #TODO Reset selected somewhere around here
        r = map(lambda x: x+'|', TimeWCommand.alias)
        a = ''.join(list(r))[:-1]

        r = map(lambda x: x+'|', list(TimeWCommand.supported_commands.keys()))
        c = ''.join(list(r))[:-1]

        s = "^("+a+"){0,1}\s{0,1}("+c+"){0,1}\s{0,1}"
        m = regex.search(s, et) if et != '' else None

        cmds = []
        arg_help = False
        if m != None and (m.groups()[0] != None or m.groups()[1] != None):
            # Cut from search_text commands we already have
            cut_pos=m.spans()[-1][-1]
            search_text = et[cut_pos:]
            self.cmp_pos=cut_pos

            if m.groups()[1] != None:
                # Skip partial command search
                arg_help = True

            else:
                # Build cmdlist
                cmds.extend(TimeWCommand.supported_commands)
        else:
            search_text = et
            cmds.extend(TimeWCommand.alias)
            cmds.extend(TimeWCommand.supported_commands)

        # Partial command completion
        b = []
        for c in cmds:
            txt_out = []
            cm = regex.search("("+search_text+")+", c)
            if cm != None:
                cm_ch = []
                for s in cm.spans():
                    cm_ch.extend(list(range(*s)))

                # Mark command parts that are matching, highlight them
                pos = 0
                hl = False
                for ch in c:
                    if pos in cm_ch:
                        if not hl or pos == 0:
                            txt_out.append(['cmp_list_hl', ''])
                            hl = True

                        txt_out[-1][1] += ch

                    else:
                        if hl or pos == 0:
                            txt_out.append(['cmp_list', ''])
                            hl = False

                        txt_out[-1][1] += ch

                    pos += 1

                # Make tulples out of list, urwid does not like list
                r = []
                for t in txt_out:
                    if type(t) == list:
                        r.append(tuple(t))
                    else:
                        r.append(t)

                cmpl = len(c) if len(c) > cmpl else cmpl
                b.append(CMPListItem(r))

        # No match show all commands
        if len(b) == 0:
            for c in cmds:
                cmpl = len(c) if len(c) > cmpl else cmpl
                b.append(CMPListItem(c))

        # Help with tags and command arguments
        if arg_help:
            ah = TimeWCommand.supported_commands[m.groups()[1]]
            cmpl = len(ah) if len(ah) > cmpl else cmpl
            b = [CMPListItem(ah)]

        #logging.debug(f"CMP Popup '{b!r}'")

        self.cmp_length = cmpl if cmpl > 0 else 1
        if self._pop_up_widget != None:
            self._pop_up_widget.update_cmp(commands=b)

    def get_edit_text(self):
        return self._edit.get_edit_text()

    def set_edit_text(self, s):
        self._edit.set_edit_text(s)
        self._edit._invalidate()

    def clear(self):
        self.set_edit_text('')
        self._edit._invalidate()

class CMPPopUp(u.PopUpTarget):
    """ Command completion PopUp """
    def __init__(self, keypress_handle):
        self._cmds = []
        self._size = 0
        """Number of items in popup"""

        self._sel_index = 0
        """Show listitem that has been selected (index)"""

        self._selected = False
        """An item has been selected"""

        b = []
        for c in TimeWCommand.alias:
            b.append(CMPListItem(c))
        self.assemble(commands=b)

        self._keypress_handle = keypress_handle
        """Catch keypress and give it to keypress_handle"""

        super(CMPPopUp, self).__init__(self._w)

    def assemble(self, commands=[]):
        self._cmds = commands
        self._body = u.SimpleListWalker([])
        for c in commands:
            c.select()
            self._body.append(c)

        self._size = self.size
        self._w = u.AttrMap(u.ListBox(self._body), 'cmp_list')

    def update_cmp(self, commands=[], sel=None):
        """Update autocomplete list"""
        self._cmds = commands
        self._body.clear()

        for i in range(0, len(commands)):
            if sel != None and i == sel:
                commands[i].select()
                self._body.append(commands[i])

            else:
                commands[i].unselect()
                self._body.append(commands[i])

            #logging.debug("com {0!r}".format(commands[i]._attrib))

    def select(self, pos_change):
        """Select autocomplete list item"""

        # Do menu looping
        if not self._selected:
            self.index = 0

        elif self.index + pos_change >= self.size:
            self.index = 0

        elif self.index + pos_change < 0:
            self.index = self.size-1

        else:
            self.index += pos_change

        self._selected = True
        self.update_cmp(self._cmds, sel=self.index)

    def unselect(self):
        """Remove selection"""
        self._selected = False
        self.index = 0
        self.update_cmp(self._cmds, sel=None)

    def get_selected(self):
        """Return selected item"""
        return self._cmds[self.index].get_text()[0]

    def keypress(self, size, key):
        """Catch keypress give it to keypress handle"""
        key = self._keypress_handle(key)

        if key:
            return super(CMPPopUp, self).keypress(size, key)

    @property
    def size(self):
        """Return number of items in popup"""
        return len(self._body)

    @property
    def index(self):
        """Return index of selected item in popup"""
        return self._sel_index

    @index.setter
    def index(self, i):
        """Select item via index"""
        self._sel_index = i
        self._selected = True

    @property
    def selected(self):
        """Return if an item has been selected"""
        self._selected = True

class CMPListItem(u.Text):
    """Command completion PopUp List Item"""
    _selectable = True
    signals = ['click']

    def __init__(self, markup,
        align: Literal['left', 'center', 'right'] = u.LEFT,
        wrap: Literal['space', 'any', 'clip', 'ellipsis'] = u.SPACE,
        layout=None):

        self._cache_maxcol = None
        self.set_text(markup)
        self.set_layout(align, wrap, layout)

        self._mrkup = markup

    def select(self):
        markup = []

        if type(self._mrkup) != str:
            for m in self._mrkup:
                if type(m) == tuple:
                    if m[0] == 'cmp_list' or m[0] == 'cmp_list_unsel':
                        markup.append(('cmp_list_sel', m[1]))

                    else:
                        markup.append(m)
                else:
                    markup.append(('cmp_list_sel', m))
        else:
            markup.append(('cmp_list_sel', self._mrkup))

        #logging.debug("sel markup '{0!r}'".format(markup))
        self.set_text(markup)

    def unselect(self):
        markup = []

        if type(self._mrkup) != str:
            for m in self._mrkup:
                if type(m) == tuple:
                    if m[0] == 'cmp_list' or m[0] == 'cmp_list_sel':
                        markup.append(('cmp_list_unsel', m[1]))

                    else:
                        markup.append(m)
                else:
                    markup.append(('cmp_list_unsel', m))
        else:
            markup.append(('cmp_list_unsel', self._mrkup))

        self.set_text(markup)

    def keypress(self, size, key):
        if self._command_map[key] != u.ACTIVATE:
            return key

        self._emit('click')

    def mouse_event(self, size, event, button, x, y, focus):
        logging.debug("CMPListItem click {0}".format(
            repr([size, event, button, x,y,focus])))
        if button != 1 or not u.util.is_mouse_press(event):
            return False

        self._emit('click')
        return True

class WidgetCLButton(CombatantButton):
    _border_char = u'─'

    def __init__(self, cmd_label=':', on_press=None, user_data=None, sm=None):
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
