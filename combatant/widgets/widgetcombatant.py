import urwid as u

import logging

class CombatantWidget:
    def __init__(self, sm=None):
        self._sm = sm

    def emit(self, signal, *args, **kwargs):
        self._sm.put(signal, *args, **kwargs)

class CombatantWidgetWrap(u.WidgetWrap, CombatantWidget):
    def __init__(self, _w, sm=None):
        CombatantWidget.__init__(self, sm=sm)
        u.WidgetWrap.__init__(self, _w)

class CombatantButton(u.Button, CombatantWidget):
    def __init__(self, _w, label='',
                           on_press=None,
                           user_data=None,
                           sm=None):

        CombatantWidget.__init__(self, sm=sm)
        #u.Button.__init__(self, )

class CombatantEdit(u.Button, CombatantWidget):
    def __init__(self, _w, sm=None):
        CombatantWidget.__init__(self, sm=sm)
        u.Edit.__init__(self, _w)

class CombatantPopUp(u.Button, CombatantWidget):
    def __init__(self, _w, sm=None):
        CombatantWidget.__init__(self, sm=sm)
        u.Edit.__init__(self, _w)

class CombatantPopUpTarget(u.Button, CombatantWidget):
    def __init__(self, _w, sm=None):
        CombatantWidget.__init__(self, sm=sm)
        u.Edit.__init__(self, _w)
