import logging

import unittest
from combatant.signalmanager import SignalManager

class SignalManagerTestCase(unittest.TestCase):
    """Test SignalManager"""
    def setUp(self):
        self.sm = SignalManager()
        logging.basicConfig(filename = 'test.log',
                            encoding = 'utf-8',
                            level = logging.DEBUG)

    def test_register_signal(self):
        self.sm.register('SigTest', 'Test desc')

    def test_connect(self):
        self.sm.register('SigTest', 'Test desc')

        def test():
            return 0

        self.sm.connect(self, 'SigTest', test)

        self.assertEqual(len(self.sm._registry['SigTest']._handlers), 1)

    def test_connect_two(self):
        self.sm.register('SigTest', 'Test desc')

        def test():
            return 0

        def test2():
            return 0

        self.sm.connect(self, 'SigTest', test)
        self.sm.connect(self, 'SigTest', test2)
        logging.debug('h {0!r}'.format(self.sm._registry['SigTest']._handlers))
        self.assertEqual(len(self.sm._registry['SigTest']._handlers), 2)

if __name__ == "__main__":
    unittest.main()
