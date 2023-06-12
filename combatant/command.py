import subprocess, re
import logging
import asyncio

class CommandError(Exception):
    def __init__(self, cmd=''):
        self.message = f"Invalid command '{cmd}'"
        super(Exception, self).__init__(self.message)

class CommandSterilizationError(Exception):
    # Naughty boi exception
    def __init__(self, match=''):
        self.message = f"Commands contains invalid symbol '{match}'"
        super(Exception, self).__init__(self.message)

class TW:
    p_stdout = subprocess.PIPE
    p_stdin = subprocess.PIPE
    p_stderr = subprocess.PIPE

    @staticmethod
    def sterilize(cmd):
        naughty_match = re.search(r"(\||;|\&|>|<|´|`)", cmd)
        cmd = re.sub(r"^((timew|timewarrior) )", '', cmd)

        if naughty_match:
            raise CommandError(naughty_match.group(0))

        else:
            # Return chopped command
            return cmd.split(' ')

    @staticmethod
    def execute(command, *args, **kwargs):
        if not 'stdout' in kwargs: kwargs['stdout'] = TW.p_stdout
        if not 'stdin' in kwargs: kwargs['stdin'] = TW.p_stdin

        proc = subprocess.Popen(command, **kwargs)
        stdout, stderr = proc.communicate()
        returncode = proc.returncode
        return (returncode, stdout, stderr)

    async def run(cmd):
        c_match = re.search(
        r'^(timew|timewarrior|)[ ]{0,1}(\-\-|)(start|stop|version|help)',
         cmd)

        if c_match:
            c = TW.sterilize(cmd)
            c.insert(0, 'timew')
            logging.debug(f"EXECUTE'{c!r}'")
            return TW.execute(c)

        else:
            raise CommandError(cmd)

