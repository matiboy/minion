import re
import multiprocessing

logger = multiprocessing.get_logger()


class BaseCommand(object):
    configuration = {
        'action': 'noop',
        'expressions': []
    }
    multi = False

    def __init__(self, configuration={}, name=''):
        self.configuration.update(configuration)
        self.name = name
        logger.info('Registering command with configuration %s', self.configuration)
        # Parse regular expressions
        print self.configuration, self.configuration['expressions']
        self.expressions = [re.compile(exp) for exp in self.configuration['expressions']]
        logger.info('Command <%s> will respond to the following expressions: %s', self.name, self.expressions)

    def understand(self, *commands):
        raise NotImplementedError('"Understand" method must be implemented in command')

    def is_blocking_command(self):
        return False

    def matches(self, command):
        commands = []
        for regular_expression in self.expressions:
            m = regular_expression.match(command)
            if m:
                if self.multi:
                    commands.append(m)
                else:
                    return m
        return commands


class BlockingCommand(BaseCommand):

    def is_blocking_command(self):
        return True
