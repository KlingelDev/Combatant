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
        sm.register('StartActivity', 'Timew started timer')
        sm.register('StopActivity', 'Timew started timer')
        sm.register('FileOpen', 'Open a file')
        sm.register('FileOpened', 'Open a file')
        sm.register('FileWrite', 'Write a file')
        sm.register('FileWritten', 'Write a file')
        sm.register('TestComplete', 'TestingCompleted')

