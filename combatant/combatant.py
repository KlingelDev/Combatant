import pudb

import os, sys
import time, re, traceback, signal

import asyncio
import logging

import urwid as u

from widgetmain import WidgetMain
from widgetbody import WidgetBody
from widgettabs import WidgetTabs
from widgetcl import WidgetCL

from command import TW, CommandSterilizationError, CommandError

class TaskCreationError(Exception):
    # Naughty boi exception
    def __init__(self, cmd=''):
        self.message = f"Cannot create task for cmd '{cmd}'"
        super(Exception, self).__init__(self.message)

class CombatantPalette:
    @staticmethod
    def colors():
        return [("normal", "black", "dark gray"),
                ("selected", "black", "light gray"),
                ("tabnormal", "black", "dark gray"),
                ("tabselected", "black", "light gray"),
                ("bg", "white", "black"),
                ("tabborder", "light gray", "black")
               ]

    @staticmethod
    def colors256():
        return [("normal", "black", "dark gray"),
                ("selected", "black", "light gray"),
                ("bg", "white", "black")
               ]

class Combatant(metaclass = u.signals.MetaSignals):
    signals = ['AppStart', 'WinChange']

    #NOTE: Deal with highest level of the Application, Interface, Files, Threads
    def __init__(self, setup=False):
        logging.debug('=====================================================')
        logging.debug('...starting.')
        self._tick = 0.1 #sec
        self._last_tick = time.time_ns()

        self._tasks = set()
        self.f = ''

        if setup:
            self.setup()

    def setup(self):
        self.ui = u.raw_display.Screen()

        self.frame = WidgetMain()

        self.asyncio_loop = asyncio.get_event_loop()
        self.aloop = u.AsyncioEventLoop(loop = self.asyncio_loop)

        logging.debug('Palette {0}'.format(repr(CombatantPalette.colors())))
        self.uloop = u.MainLoop(self.frame,
                                CombatantPalette.colors(),
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
        u.register_signal(WidgetMain, WidgetMain.signals)
        u.register_signal(WidgetTabs, WidgetTabs.signals)
        u.register_signal(WidgetBody, WidgetBody.signals)
        u.register_signal(WidgetCL, WidgetCL.signals)
        u.register_signal(self, self.signals)

        u.connect_signal(self.frame.body, 'Dirty', self.draw_screen)
        u.connect_signal(self.frame.cl, 'Dirty', self.draw_screen)
        u.connect_signal(self.frame.cl, 'CMD', self.signal_cmd)
        u.connect_signal(self.frame, 'Quit', self.signal_quit)

        u.connect_signal(self, 'WinChange', self.frame.body.win_change)
        u.connect_signal(self, 'WinChange', self.frame.tabs.win_change)
        u.connect_signal(self, 'WinChange', self.frame.cl.win_change)

        u.connect_signal(self.frame.tabs, 'TabSwitch', self.frame.body.tab_switch)

        u.connect_signal(self, 'AppStart', self.frame.app_start)

    def run(self):
        try:
            # Do what needs to be done at first application start
            u.emit_signal(self, 'AppStart')

            # Let widgets know about winsize
            cols, rows = self.ui.get_cols_rows()
            u.emit_signal(self, 'WinChange', (cols, rows))

            self.uloop.run()

        except u.ExitMainLoop as exc:
            logging.debug('quitting.')

        except BaseException as exc:
            traceback.print_exception(exc, limit=1, file=sys.stdout)
            self.signal_quit()

    def signal_cmd(self, cmd):
        # TODO add commands to switch tabs
        logging.debug(f'CMD {cmd!r}')
        task = None
        cquit_match = re.search('^[qQ]uit', cmd)
        if cquit_match:
            self.signal_quit()
            return 0

        try:
            task = self.asyncio_loop.create_task(TW.run(cmd), name=f'TWCMD {cmd!r}')

            if isinstance(task, asyncio.Task):
                task.add_done_callback(self.cmd_result)
                self._tasks.add(task)

            else:
                raise TaskCreationError(cmd)

        except BaseException as exc:
            logging.debug(f"Failed to create task for cmd '{cmd}'")
            exc = traceback.format_exception(exc, limit=4, chain=True)
            for l in exc:
                if len(l): logging.debug('{0}'.format(l[:-1]))

    def cmd_result(self, task):
        try:
            r = task.result()
            logging.debug(
                'Cmd result: {0} len out ({1}); {2}...'.format(r[0],
                                                               len(r[1]),
                                r[1][:200 if len(r[1])>=200 else len(r[1])]))

        except CommandError as exc:
            exc = traceback.format_exception(exc, limit=4, chain=True)
            for l in exc:
                if len(l): logging.debug('{0}'.format(l[:-1]))

        except BaseException as exc:
            logging.debug(f'Task Error Traceback')
            exc = traceback.format_exception(exc, limit=4, chain=True)
            for l in exc:
                if len(l): logging.debug('{0}'.format(l[:-1]))

        self._tasks.discard(task)

    def draw_screen(self):
        logging.debug('draw screen')
        self.uloop.draw_screen()

    def signal_quit(self):
        logging.debug('sig quit')
        raise u.ExitMainLoop()

    def signal_winch(self):
        cols, rows = self.ui.get_cols_rows()
        logging.debug('winch: %d x %d' % (cols, rows))
        u.emit_signal(self, 'WinChange', (cols, rows))

