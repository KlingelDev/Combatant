import os, sys
import time, traceback, signal

from io import StringIO

import asyncio
import logging
import regex
import datetime

import urwid as u

from widgets import (WidgetBody,
                     WidgetMain,
                     WidgetTabs,
                     WidgetCL,
                     WidgetCLEdit)

from signalmanager import SignalManager
from signals import CombatantSignals

from twcommand import TimeW, CommandSterilizationError, CommandError
from twcommand import TimeWCommand as twc

from util.file import File, NoFileError

from activity import Activity

class TaskCreationError(Exception):
    def __init__(self, cmd=''):
        self.message = f"Cannot create task for cmd '{cmd}'"
        super(Exception, self).__init__(self.message)

class CombatantPalette:
    @staticmethod
    def colors():
        return [("normal", "black", "dark gray"),
                ("selected", "black", "light gray"),
                ("tabnormal", "black", "dark gray"),

                ('cmp_list', 'white', 'dark blue'),
                ('cmp_list_hl', 'white,standout', 'dark blue'),
                ('cmp_list_sel', 'black', 'dark gray'),
                ('cmp_list_unsel', 'white', 'dark blue'),

                ('activity_runnning', 'white', 'dark green'),
                ('activity_stopped', 'black', 'dark red'),

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

"""
Combatant
"""
class Combatant:
    """
    Deal with highest level of the Application, Interface, Files, Threads
    """
    setup: bool
    """Perform setup"""

    def __init__(self, setup=False, unittest=False):
        logging.debug('=====================================================')
        logging.debug('...starting.')

        self.unittest = unittest

        self._tick = .1666 #sec
        self._last_tick = time.time_ns()

        self._tasks = set()

        if setup:
            self.setup()

    def setup(self):
        if self.unittest:
            # Redirect stdout into nothing for unittest
            stdout_buff = StringIO()
            stdin_buff = StringIO()
            self.ui = u.raw_display.Screen(output=stdout_buff)

        else:
            self.ui = u.raw_display.Screen()

        self.signal_manager = SignalManager()
        CombatantSignals.register_signals(sm=self.signal_manager)

        self.frame = WidgetMain(sm=self.signal_manager)

        self.asyncio_loop = asyncio.get_event_loop()
        self.aloop = u.AsyncioEventLoop(loop = self.asyncio_loop)

        #loop.screen.set_terminal_properties(colors=256)

        logging.debug('Palette {0}'.format(repr(CombatantPalette.colors())))
        self.uloop = u.MainLoop(self.frame,
                                CombatantPalette.colors(),
                                screen = self.ui,
                                handle_mouse = True,
                                event_loop = self.aloop,
                                pop_ups = True)

        # SIGhandler setup
        self.asyncio_loop.add_signal_handler(signal.SIGWINCH, self.signal_winch)
        self.asyncio_loop.add_signal_handler(signal.SIGTERM, self.signal_quit)
        self.asyncio_loop.add_signal_handler(signal.SIGINT, self.signal_quit)
        self.asyncio_loop.add_signal_handler(signal.SIGQUIT, self.signal_quit)

        # Register and plug signals
        # self.signal_manager.connect(self.frame.body, 'Dirty', self.draw_screen)
        # self.signal_manager.connect(self.frame.cl, 'Dirty', self.draw_screen)
        self.signal_manager.connect(self.frame.cl.edit_line, 'Dirty', self.draw_screen)
        self.signal_manager.connect(self.frame.cl, 'CMD', self.signal_cmd)
        self.signal_manager.connect(self.frame, 'Quit', self.signal_quit)

        self.signal_manager.connect(self, 'FileOpen', self.file_open)
        self.signal_manager.connect(self, 'FileWrite', self.file_write)

        self.signal_manager.connect(self, 'WinChange', self.frame.body.win_change)
        self.signal_manager.connect(self, 'WinChange', self.frame.tabs.win_change)
        self.signal_manager.connect(self, 'WinChange', self.frame.cl.win_change)

        self.signal_manager.connect(self.frame.tabs, 'TabSwitch',
                                    self.frame.body.tab_switch)

        self.signal_manager.connect(self, 'AppStart', self.frame.app_start)
        self.signal_manager.connect(self, 'AppStart', self.app_start)

    def run(self):
        try:
            # Do what needs to be done at first application start
            self.signal_manager.put('AppStart')

            # Let widgets know about winsize
            cols, rows = self.ui.get_cols_rows()
            self.signal_manager.put('WinChange', (cols, rows))

            # Setup tick
            self.uloop.set_alarm_in(self._tick, self.tick)

            self.uloop.run()

        except u.ExitMainLoop as exc:
            logging.debug('quitting.')

        except BaseException as exc:
            traceback.print_exception(exc, limit=1, file=sys.stdout)
            self.signal_quit()

    def tick(self, c, u):
        """ Perform per `tick` """
        self.signal_manager.process()

        self.uloop.set_alarm_in(self._tick, self.tick)

    def app_start(self):
        """ Perform at AppStart """
        #self.signal_cmd('tags')
        #status self.signal_cmd('')

    def signal_cmd(self, cmd):
        # TODO add commands to switch tabs
        logging.debug(f'CMD {cmd!r}')
        task = None
        cquit_match = regex.search('^[qQ]uit', cmd)
        if cquit_match:
            self.signal_quit()
            return 0

        try:
            task = self.asyncio_loop.create_task(TimeW.run(cmd),
                                                 name=f'TimeWCMD {cmd!r}')

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

        finally:
            return 0

    def cmd_result(self, task):
        r = None
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

        finally:
            # Create Activity objects for display
            self._tasks.discard(task)
            if r and r[0] == 0:
                logging.debug('result: {0!r}'.format(r[1]))
                resstr = r[1].decode('utf-8')

                m = regex.match(twc.start_pattern, resstr)

                if m:
                    logging.debug('start match: {0!r}'.format(m.groups()))
                    a = Activity(status='tracking',
                                 started=m.groups()[1])
                    self.signal_manager.put('StartActivity', a)

                m = regex.match(twc.stop_pattern, resstr)

                if m:
                    logging.debug('stop match: {0!r}'.format(m.groups()))
                    a = Activity(status='recorded',
                                 started=m.groups()[1])
                    self.signal_manager.put('StopActivity', a)


    def file_open(self, f):
        """Create a task that opens a file"""
        logging.debug(f'File open {f!r}')
        task = None

        try:
            task = self.asyncio_loop.create_task(File.open(f),
                                                 name=f'FileOpen {f!r}')

            if isinstance(task, asyncio.Task):
                task.add_done_callback(self.file_open_result)
                self._tasks.add(task)

            else:
                # TODO raise File exception
                pass

        except BaseException as exc:
            logging.debug(f"Failed to create task for file open '{f}'")
            exc = traceback.format_exception(exc, limit=4, chain=True)
            for l in exc:
                if len(l): logging.debug('{0}'.format(l[:-1]))

        finally:
            return 0

    def file_write(self, f, c):
        """Create a task that writes a file"""
        logging.debug(f'File write {f!r}')
        task = None

        try:
            task = self.asyncio_loop.create_task(File.write(f, c),
                                                 name=f'FileWrite {f!r}')

            if isinstance(task, asyncio.Task):
                task.add_done_callback(self.file_open_result)
                self._tasks.add(task)

            else:
                # TODO raise File exception
                pass

        except BaseException as exc:
            logging.debug(f"Failed to create task for file write '{f}'")
            exc = traceback.format_exception(exc, limit=4, chain=True)
            for l in exc:
                if len(l): logging.debug('{0}'.format(l[:-1]))

        finally:
            return 0

    def file_open_result(self, task):
        try:
            r = task.result()
            if type(r) == str:
                logging.debug(
                    'File open result: len {0}; {1}...'.format(len(r[0]),
                                    r[0][:200 if len(r[0])>=200 else len(r[0])]))

            elif r == 0:
                logging.debug('File written: {r!r}')

        except BaseException as exc:
            logging.debug(f'File Error Traceback')
            exc = traceback.format_exception(exc, limit=4, chain=True)
            for l in exc:
                if len(l): logging.debug('{0}'.format(l[:-1]))

        finally:
            self._tasks.discard(task)
            if r:
                self.signal_manager.put('FileOpened', r)

            return 0

    def draw_screen(self):
        logging.debug('draw screen')
        self.uloop.draw_screen()

    def signal_quit(self, *arg):
        logging.debug('sig quit. Bye!')
        raise u.ExitMainLoop()

    def signal_winch(self):
        cols, rows = self.ui.get_cols_rows()
        logging.debug('winch: {0} x {1}'.format(cols, rows))
        self.signal_manager.put('WinChange', (cols, rows))

