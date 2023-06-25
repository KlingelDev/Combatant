import sys

import argparse
import logging

from combatant import Combatant

"""
Combatant Main
"""
def main(combatant_cfgdir=None):
    logging.basicConfig(
        filename = 'debug.log', encoding = 'utf-8', level = logging.DEBUG)
    a = Combatant(setup=True, combatant_cfgdir=combatant_cfgdir)
    a.run()
    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Combatant interface for timewarrior')
    parser.add_argument('-c', '--configdir', dest='combatant_cfgdir',
                        help='Configuration directory')

    cfgdir = None
    args = parser.parse_args()
    if args.combatant_cfgdir:
        cfgdir = args.combatant_cfgdir

    main(combatant_cfgdir=cfgdir)
