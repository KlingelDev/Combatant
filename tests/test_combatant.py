import os
import pytest
import logging
import unittest
from combatant.combatant import Combatant

class CombatantTestCase(unittest.TestCase):
    """Test Combatant"""
    def setUp(self):
        self.c = Combatant(setup=True, unittest=True)
        logging.basicConfig(filename = 'test.log',
                            encoding = 'utf-8',
                            level = logging.DEBUG)

    def test_app_start(self):
        self.c.app_start()

    def test_cmd_twhelp(self):
        self.c.signal_cmd('timew help')

    async def test_run_stop(self):
        self.c.uloop.set_alarm_in(0.001, self.c.signal_quit)
        await self.c.run()

    async def test_open_file(self):
        teststr = 'This is a test\n'

        file = os.path.join(os.getcwd(), 'test.txt')

        f = open(file, 'w', encoding='utf-8')
        f.write(teststr)
        f.close()

        class FH:
            def __init__(self):
                self.r = ''

            def fr_handle(self, r):
                logging.debug(f"fhandle '{r}'")
                self.r = r

        fhandle=FH()

        self.c.signal_manager.connect(self, 'FileOpened', fhandle.fr_handle)

        self.c.signal_manager.put('FileOpen', file)
        self.c.uloop.set_alarm_in(1, self.c.signal_quit)
        await self.c.run()

        assert fhandle.r == teststr

        os.remove(file)

    async def test_write_and_open_file(self):
        teststr = 'This is a test\n'
        file = os.path.join(os.getcwd(), 'test.txt')

        class FH:
            def __init__(self):
                self.r = ''

            def fr_handle(self, r):
                logging.debug(f"fhandle '{r}'")
                self.r = r

        fhandle=FH()

        self.c.signal_manager.connect(self, 'FileOpened', fhandle.fr_handle)

        self.c.signal_manager.put('FileOpen', file)
        self.c.signal_manager.put('FileWrite', file, teststr)

        self.c.uloop.set_alarm_in(1, self.c.signal_quit)
        await self.c.run()

        assert fhandle.r == teststr

        os.remove(file)
