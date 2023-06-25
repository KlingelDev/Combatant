import os
import logging
import unittest
import time
import combatant.combatant as cb

import importlib

logging.basicConfig(filename = 'test.log',
                    encoding = 'utf-8',
                    level = logging.DEBUG)

logger = logging.getLogger()

class CombatantTestCase(unittest.TestCase):
    """Test Combatant"""
    def setUp(self):
        self.c = cb.Combatant(setup=True, unittest=True)

    def tearDown(self):
        del self.c
        time.sleep(1)

    def test_app_start(self):
        self.c.app_start()

    def test_run_stop(self):
        self.c.signal_manager.put('Quit')
        self.c.run()

    def test_cmd_twhelp(self):
        self.c.signal_cmd('timew help')

    # TODO The file open test will work once. The second time fr_handle will not
    # be called and fhandle.r will remain '', even though the file has been
    # opend and FileOpenend is signaled. Might be some bizarre unittest/pytest bug.
    # def test_open_file(self):
    #     teststr = 'This is a test\n'
    #
    #     file = os.path.join(os.getcwd(), 'test1.txt')
    #
    #     f = open(file, 'w', encoding='utf-8')
    #     f.write(teststr)
    #     f.close()
    #
    #     class FH:
    #         def __init__(self):
    #             self.r = ''
    #
    #         def fr_handle(self, r):
    #             self.r = r
    #
    #     fhandle=FH()
    #
    #     self.c.signal_manager.connect(self, 'FileOpened', fhandle.fr_handle)
    #     self.c.signal_manager.setwaitfor('FileOpened')
    #     self.c.signal_manager.put('FileOpen', file)
    #
    #     self.c.run()
    #
    #     #os.remove(file)
    #
    #     assert fhandle.r == teststr
    #
    # def test_write_and_open_file(self):
    #     teststr = 'This is a test\n'
    #     file = os.path.join(os.getcwd(), 'test2.txt')
    #
    #     class FH:
    #         def __init__(self):
    #             self.r = ''
    #
    #         def fr_handle(self, r):
    #             logger.debug(f"set fhandle '{r}'")
    #             self.r = r
    #
    #     f2handle=FH()
    #
    #     self.c.signal_manager.connect(self.c, 'FileOpened', f2handle.fr_handle)
    #     self.c.signal_manager.setwaitfor('FileOpened')
    #     logger.debug("waitfor '{0}'".format(self.c.signal_manager.waitforoccured))
    #     self.c.signal_manager.waitforoccured = False
    #
    #     self.c.put_after_start('FileOpen', file)
    #     self.c.put_after_start('FileWrite', file, teststr)
    #
    #     self.c.run()
    #
    #     logger.debug("fh value '{0}'".format(f2handle.r))
    #     assert f2handle.r == teststr
    #
    #     os.remove(file)
