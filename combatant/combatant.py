import pudb
import os, sys, traceback, signal, time

import asyncio
import logging

import urwid as u

from widgetmain import WidgetMain
from widgetbody import WidgetBody
from widgettabs import WidgetTabs
from widgetcl import WidgetCL

class Combatant(metaclass = u.signals.MetaSignals):
    signals = ['Setup', 'WinChange']
    #NOTE: Deal with highest level of the Application, Interface, Files, Threads
    def __init__(self, setup=False):
        logging.debug('...starting.')
        self._tick = 0.1 #sec
        self._last_tick = time.time_ns()

        if setup:
            self.setup()

    def setup(self):
        self.ui = u.raw_display.Screen()

        self.frame = WidgetMain()

        self.asyncio_loop = asyncio.get_event_loop()
        self.aloop = u.AsyncioEventLoop(loop = self.asyncio_loop)

        self.uloop = u.MainLoop(self.frame,
                                #unhandled_input = self.unhandled_input,
                                handle_mouse = True,
                                event_loop = self.aloop,
                                pop_ups = True
                               )

        # SIGhandler setup
        self.asyncio_loop.add_signal_handler(signal.SIGWINCH, self.signal_winch)
        self.asyncio_loop.add_signal_handler(signal.SIGTERM, self.signal_quit)
        self.asyncio_loop.add_signal_handler(signal.SIGINT, self.signal_quit)
        self.asyncio_loop.add_signal_handler(signal.SIGQUIT, self.signal_quit)

        # Setup tick
        #self.uloop.set_alarm_in(1, self.frame.update_body)

        # Register and plug urwid/widget signals
        u.register_signal(WidgetBody, ['Dirty', 'Quit'])
        u.register_signal(WidgetCL, ['Dirty', 'Quit'])
        u.register_signal(self, ['WinChange'])

        u.connect_signal(self.frame.body, 'Dirty', self.draw_screen)
        u.connect_signal(self.frame.body, 'Quit', self.signal_quit)

        u.connect_signal(self, 'WinChange', self.frame.body.win_change)
        u.connect_signal(self, 'WinChange', self.frame.tabs.win_change)
        u.connect_signal(self, 'WinChange', self.frame.cl.win_change)

    def run(self):
        try:
            # Do what needs to be done at first application start
            u.emit_signal(self, 'Setup')

            # Let widgets know about winsize
            cols, rows = self.ui.get_cols_rows()
            u.emit_signal(self, 'WinChange', (cols, rows))

            self.uloop.run()

        except u.ExitMainLoop as exc:
            logging.debug('quitting.')

        except BaseException as exc:
            traceback.print_exception(exc, limit=2, file=sys.stdout)
            self.signal_quit()

    def draw_screen(self):
        logging.debug('draw screen')
        self.uloop.draw_screen()


    def signal_quit(self):
        logging.debug('sig quit')
        raise u.ExitMainLoop()

    def unhandled_input(self):
        if key == 'q' or key == 'Q':
            logging.debug('pressed Q')
            self.signal_quit()

    def signal_winch(self):
        cols, rows = self.ui.get_cols_rows()
        logging.debug('winch: %d x %d' % (cols, rows))
        u.emit_signal(self, 'WinChange', (cols, rows))

