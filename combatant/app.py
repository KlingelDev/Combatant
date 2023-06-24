import logging

from combatant import Combatant

"""
Combatant Main
"""
def main():
    logging.basicConfig(
        filename = 'debug.log', encoding = 'utf-8', level = logging.DEBUG)
    a = Combatant(setup=True)
    a.run()
    return 0

if __name__ == '__main__':
    main()
