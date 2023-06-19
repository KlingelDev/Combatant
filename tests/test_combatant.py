import logging
import unittest
from combatant.combatant import Combatant

class CombatantTestCase(unittest.TestCase):
    """Test Combatant"""
    def setUp(self):
        self.c = Combatant(setup=True)

    def test_app_start(self):
        self.c.app_start()
