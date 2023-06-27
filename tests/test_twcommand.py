import os
import logging
import unittest
import pytest
import urwid as u
import asyncio

from combatant.twcommand import TimeW as tw
from combatant.twcommand import CommandSterilizationError, CommandError

logging.basicConfig(filename = 'test.log',
                    encoding = 'utf-8',
                    level = logging.DEBUG)

logger = logging.getLogger()

class TWCommandTestCase(unittest.TestCase):
    """Test TWCommand"""
    def setUp(self):
        self.l = asyncio.get_event_loop()

    def test_cmd1(self):
        t = self.l.create_task(tw.run('timew help'), name="TEST")
        self.l.run_until_complete(t)
        assert t.result()[0] == 0

    def test_cmd2(self):
        t = self.l.create_task(tw.run('timewarrior help'), name="TEST")
        self.l.run_until_complete(t)
        assert t.result()[0] == 0

    def test_cmd3(self):
        with pytest.raises(CommandSterilizationError) as eml:
            t = self.l.create_task(tw.run('timew help | a bad boi'), name="TEST")
            self.l.run_until_complete(t)

    def test_cmd4(self):
        with pytest.raises(CommandSterilizationError) as eml:
            t = self.l.create_task(tw.run('timew help; a bad boi'), name="TEST")
            self.l.run_until_complete(t)

    def test_cmd5(self):
        with pytest.raises(CommandSterilizationError) as eml:
            t = self.l.create_task(tw.run('timew help >> a bad boi'), name="TEST")
            self.l.run_until_complete(t)

    def test_cmd6(self):
        with pytest.raises(CommandError) as eml:
            t = self.l.create_task(tw.run('sudo ls /root'), name="TEST")
            self.l.run_until_complete(t)
