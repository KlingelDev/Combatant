import os
import logging
import unittest
import combatant.combatant as cb
import asyncio
import pytest
import urwid as u

logging.basicConfig(filename = 'test.log',
                    encoding = 'utf-8',
                    level = logging.DEBUG)

logger = logging.getLogger()

class CombatantTestCase(unittest.TestCase):
    """Test Combatant"""
    def setUp(self):
        self.c = cb.Combatant(setup=True, unittest=True)

    def tearDown(self):
        pass

    def test_app_start(self):
        assert self.c.app_start() == None

    def test_cmd_twhelp(self):
        assert self.c.signal_cmd('timew help') == 0

    def test_signal_cmd1(self):
        with pytest.raises(u.ExitMainLoop) as eml:
            self.c.signal_cmd('quit')

    def test_signal_cmd2(self):
        assert self.c.signal_cmd("timew help") == 0

    def test_cmd_result1(self):
        async def afunc(): return (0, b'fu')

        l = asyncio.get_event_loop()
        t = l.create_task(afunc(), name="TEST")
        self.c._tasks.add(t)
        l.run_until_complete(t)
        self.c.cmd_result(t)

        f = False
        for s in self.c.signal_manager._que:
            if s[0] == 'StartActivity' or s[0] == 'StopActivity':
                f = True
                break

        assert f == False

    def test_cmd_result_starta(self):
        async def afunc(): return (0, b'Tracking \n   Started 2023-06-26T19:50:56')

        l = asyncio.get_event_loop()
        t = l.create_task(afunc(), name="TEST")
        self.c._tasks.add(t)
        l.run_until_complete(t)
        self.c.cmd_result(t)

        f = False
        for s in self.c.signal_manager._que:
            if s[0] == 'StartActivity':
                f = True
                break

        assert f

    def test_cmd_result_stopa(self):
        async def afunc(): return (0, b'Recorded  \n  Started 2023-06-26T19:50:56')

        l = asyncio.get_event_loop()
        t = l.create_task(afunc(), name="TEST")
        self.c._tasks.add(t)
        l.run_until_complete(t)
        self.c.cmd_result(t)

        f = False
        for s in self.c.signal_manager._que:
            if s[0] == 'StopActivity':
                f = True
                break

        assert f

    def test_file_open_result1(self):
        async def afunc(): return ('test.txt', 'TEST')

        l = asyncio.get_event_loop()
        t = l.create_task(afunc(), name="TEST")
        self.c._tasks.add(t)
        l.run_until_complete(t)
        self.c.file_open_result(t)

        f = False
        for s in self.c.signal_manager._que:
            if s[0] == 'FileOpened' or s[1][1] == 'TEST':
                f = True
                break

        assert f

    def test_file_open_result2(self):
        """File written"""
        async def afunc(): return ('test.txt', 0)

        l = asyncio.get_event_loop()
        t = l.create_task(afunc(), name="TEST")
        self.c._tasks.add(t)
        l.run_until_complete(t)
        assert self.c.file_open_result(t) == 0

