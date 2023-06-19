import urwid as u

import logging

class CombatantWidget:
    _selectable = True
    """
    Superclass for Widgets used by Combatant
    """
    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        if 'sm' in kwargs:
            obj._sm = kwargs['sm']
            obj._w = None
        return obj

    def __init__(self, sm=None):
        if sm != None:
            self._sm = sm

    def emit(self, signal, *args, **kwargs):
        self._sm.put(signal, *args, **kwargs)

    def connect_signal(self, caller, name, handler, **kwargs):
        self._sm.connect(caller, name, handler, **kwargs)

    def focus(self):
        """Sets focus on main widget _w, override will be needed"""
        self._w.focus_position=0

"""
Urwid facades
"""
class CombatantWidgetWrap(u.WidgetWrap, CombatantWidget):
    #sm: SignalManager
    """Signal Manager"""
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

class CombatantEdit(u.Edit, CombatantWidget):
    def __init__(self, _w, sm=None):
        CombatantWidget.__init__(self, sm=sm)
        u.Edit.__init__(self, _w)

class CombatantPopUpLauncher(u.PopUpLauncher, CombatantWidget):
    def __init__(self, _w, sm=None):
        CombatantWidget.__init__(self, sm=sm)
        u.PopUpLauncher.__init__(self, _w)

class CombatantPopUpTarget(u.PopUpTarget, CombatantWidget):
    def __init__(self, _w, sm=None):
        CombatantWidget.__init__(self, sm=sm)
        u.PopUpTarget.__init__(self, _w)
