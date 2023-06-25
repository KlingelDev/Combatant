import sys, os

import regex
import configparser

import logging

class ConfigKeyError(Exception):
    def __init__(self, k=''):
        self.message = f"Key not found in Config '{k}'"
        super(Exception, self).__init__(self.message)

class ConfigEnv:
    """Filenames and folder for combatant configuration"""
    config_path = '~/.combatant'
    config_name = 'combatant.config'

class CombatantConfig:
    """Manage Combatant configuration file"""
    def __init__(self, cfgpath, sm=None):
        self.sm = sm
        self.c = configparser.ConfigParser(allow_no_value=True)
        """Config parser obj"""

        if cfgpath == None:
            self.cfg_path = ConfigEnv.config_path
        else:
            self.cfg_path = cfgpath

        self.cfg_path = os.path.expanduser(self.cfg_path)
        self.cfg_file = os.path.join(self.cfg_path, ConfigEnv.config_name)
        """config file name"""

        # Create
        if not os.path.isdir(self.cfg_path) and self.cfg_path != None:
            os.mkdir(self.cfg_path)

        if not os.path.isfile(self.cfg_file):
            os.mknod(self.cfg_file)

        if self.sm != None:
            self.sm.connect(self, 'FileOpened', self.parse_conf)

    def load(self):
        """Load config file"""
        self.sm.put('FileOpen', self.cfg_file)

    def parse_conf(self, cfg_file):
        """Parse config file contents"""
        logging.debug(f'parse conf')
        if cfg_file[1] == self.cfg_file:
            self.c.read_str(self.cfg_file)

    def save(self):
        """Write configfile to disk"""
        c = self.c.tostr(self.cfg_path)
        self.sm.put('FileWrite', self.cfg_file, c)

    def v(self, n):
        """Get value of a given name"""
        if n in self.c:
            return self.c[n]

        else:
            raise ConfigKeyError

