import logging
import unittest
from combatant.combatant import Combatant

class CombatantTestCase(unittest.TestCase):
    """Test Combatant"""
    def setUp(self):
        self.c = Combatant(setup=True, unittest=True)

    def test_app_start(self):
        self.c.app_start()

    def test_cmd_twhelp(self):
        self.c.signal_cmd('timew help')

    def test_run_stop(self):
        self.c.uloop.set_alarm_in(0.001, self.c.signal_quit)
        self.c.run()
