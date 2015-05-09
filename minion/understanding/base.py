import re
import multiprocessing

logger = multiprocessing.get_logger()


class UnderstandingCommand(object):
    used = False
    def __init__(self, action, message):
        self.action = action
        self.message = message

    def __iter__(self):
        return self

    def next(self):
        if not self.used:
            self.used = True
            return self

        raise StopIteration

    def publish(self, nervous_system):
        nervous_system.publish(self.action, self.message)


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

    def understand(self, nervous_system, *commands):
        actions = self._understand(*commands)
        logger.debug(actions)
        for action in actions:
            logger.debug(action)
            action.publish(nervous_system)

    def _understand(self, *commands):
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
