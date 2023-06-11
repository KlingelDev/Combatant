import subprocess
import logging
import time
import asyncio

class TW:
    @staticmethod
    def run(command, *args, **kwargs):
        scmd = TW.sanatize(command)
        proc = subprocess.Popen(scmd, **kwargs)
        stdout, stderr = proc.communicate()
        returncode = proc.returncode
        return (returncode, stdout, stderr)

    @staticmethod
    def sanatize(cmd):
        out = cmd
        return out

    @staticmethod
    async def help():
        logging.debug('async help')
        result = TW.run(['timew', 'help'], stdout=subprocess.PIPE,
                                           stdin=subprocess.PIPE)
        return result

    @staticmethod
    async def version():
        logging.debug('async version')
        result = TW.run(['timew', '--version'], stdout=subprocess.PIPE,
                                                stdin=subprocess.PIPE)
        return result

