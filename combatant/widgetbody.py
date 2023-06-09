import urwid as u
import logging

class WidgetBody(u.WidgetWrap, metaclass = u.signals.MetaSignals):
    signals = ['Quit', 'Dirty']

    def __init__(self):
        self.i = 150
        self._w = u.Filler(u.Pile([
                u.Text('-'),
            ]))
        super(WidgetBody, self).__init__(self._w)

    def update(self, _loop, _data):
        self.i -= 1
        #print(str(self.i) + '\n')
        self._w = u.Filler(u.Pile([
                u.Text(str(self.i)),
            ]))

        u.emit_signal(self, 'Dirty')
        #_loop.set_alarm_in(1, self.update)

    def win_change(self, colrows):
        cols, rows = colrows
