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
        self.assertEqual(len(self.sm._registry['SigTest']._handlers), 2)

    def test_put(self):
        self.sm.register('SigTest', 'Test desc')

        def test():
            return 0

        self.sm.connect(self, 'SigTest', test)
        self.sm.put('SigTest')

    def test_process1(self):
        """With callback on caller"""
        self.sm.register('SigTest', 'Test desc')

        def test(a):
            return 2

        class A:
            def __init__(self):
                self.x = 0

            def callback(self, r):
                self.x = r
                return self.x

        a = A()

        self.sm.connect(a, 'SigTest', test)
        self.sm.put('SigTest', 1)
        self.sm.process()

        self.assertEqual(a.x, 2)

    def test_process1a(self):
        """No callback on caller"""
        self.sm.register('SigTest', 'Test desc')

        def test(a):
            return 2

        class A:
            def __init__(self):
                self.x = 6

        a = A()

        self.sm.connect(a, 'SigTest', test)
        self.sm.put('SigTest', 1)
        self.sm.process()

        self.assertEqual(a.x, 6)

    def test_process2(self):
        """Two callbacks"""
        self.sm.register('SigTest', 'Test desc')

        def test1(a):
            return a

        def test2(a):
            return a+2

        class A:
            def __init__(self):
                self.x = 0

            def callback(self, r):
                self.x = r
                return self.x

        a = A()
        b = A()

        self.sm.connect(a, 'SigTest', test1)
        self.sm.connect(b, 'SigTest', test2)

        self.sm.put('SigTest', 1)
        self.sm.process()

        self.assertEqual(a.x, 1)
        self.assertEqual(b.x, 3)

if __name__ == "__main__":
    unittest.main()
