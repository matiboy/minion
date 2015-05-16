from . import functions
import clint.textui

for name, color in {'error': 'red', 'info': 'cyan', 'success': 'green', 'warn': 'yellow'}.iteritems():
    vars()['console_{}'.format(name)] = functions.compose(clint.textui.puts, getattr(clint.textui.colored, color))
