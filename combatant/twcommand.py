import subprocess, re, regex
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

class TimeWCommand:
    """
    Available/implemented timew commands. Information for command completion.
    """
    alias = ('timew', 'timewarrior')
    supported_commands = {
     'annotate': ('@<id> [@<id> ...] <annotation>'),
     'cancel': (),
     'config': ("[<name> [<value> | '']]"),
     'continue': ('[@<id>] [<date>|<interval>]'),
     'day': ('[<interval>] [<tag> ...]'),
     'delete': ('@<id> [@<id> ...]'),
     'diagnostics': (''),
     'export': ('[<interval>] [<tag> ...]'),
     'extensions': (''),
     'gaps': ('[<interval>] [<tag> ...]'),
     'get': ('<DOM> [<DOM> ...]'),
     'help': ('[<command> | dates | dom | durations | hints | ranges]'),
     'join': ('@<id> @<id>'),
     'lengthen': ('@<id> [@<id> ...] <duration>'),
     'modify': ('(start|end) @<id> <date>'),
     'month': ('[<interval>] [<tag> ...]'),
     'move': ('@<id> <date>'),
     #TODO make this work
     #'':('[report] <report> [<interval>] [<tag> ...]'),
     'shorten': ('@<id> [@<id> ...] <duration>'),
     'show': (''),
     'split': ('@<id> [@<id> ...]'),
     'start': ('[<date>] [<tag> ...]'),
     'stop': ('[<tag> ...]'),
     'summary': ('[<interval>] [<tag> ...]'),
     'tag': ('@<id> [@<id> ...] <tag> [<tag> ...]'),
     'tags': ('[<interval>] [<tag> ...]'),
     'track': ('<interval> [<tag> ...]'),
     'undo': (''),
     'untag': ('@<id> [@<id> ...] <tag> [<tag> ...]'),
     'week': ('[<interval>] [<tag> ...]')
    }

class TimeW:
    """
    Static Class with methods that control timewarrior.
    """
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
        if not 'stdout' in kwargs: kwargs['stdout'] = TimeW.p_stdout
        if not 'stdin' in kwargs: kwargs['stdin'] = TimeW.p_stdin

        proc = subprocess.Popen(command, **kwargs)
        stdout, stderr = proc.communicate()
        returncode = proc.returncode
        return (returncode, stdout, stderr)

    async def run(cmd):
        c_match = re.search(
        # TODO get stuff from TimeWCommands
        r'^(timew|timewarrior|)[ ]{0,1}(\-\-|)(start|stop|version|help)',
         cmd)

        if c_match:
            c = TimeW.sterilize(cmd)
            c.insert(0, 'timew')
            logging.debug(f"EXECUTE'{c!r}'")
            return TimeW.execute(c)

        else:
            raise CommandError(cmd)

