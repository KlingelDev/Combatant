import pudb
import logging

from combatant import Combatant

def main():
    logging.basicConfig(filename = 'debuglog', encoding = 'utf-8', level =
                        logging.DEBUG)
    a = CombatantApp(setup=True)
    a.run()

if __name__ == '__main__':
    main()
