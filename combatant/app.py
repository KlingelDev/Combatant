import pudb
import logging

from combatant import Combatant

"""
Combatant Main
"""
def main():
    logging.basicConfig(filename = 'debug.log', encoding = 'utf-8', level =
                        logging.DEBUG)
    a = Combatant(setup=True)
    a.run()

if __name__ == '__main__':
    main()
