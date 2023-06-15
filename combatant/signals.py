class CombatantSignals:
    @staticmethod
    def register_signals(sm=None):
        sm.register('CMDMode', 'Enter/exit command mode')
        sm.register('CMD', 'Execute command')
        sm.register('TabSwitch', 'Switch tabs')
        sm.register('AppStart', 'Initiates the application')
        sm.register('WinChange', 'Windows size change')
        sm.register('Dirty', 'Forces draw_screen()')
        sm.register('Quit', 'Exit the application')
        sm.register('Test', 'test')

