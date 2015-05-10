import re
import multiprocessing
from . import errors

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


class Noop(object):
    def __iter__(self):
        return self

    def next(self):
        raise StopIteration


class BaseCommand(object):
    configuration = {
        'action': 'noop',
        'expressions': []
    }
    multi = False

    def __init__(self, configuration={}, name=''):
        self.configuration = self.configuration.copy()
        self.configuration.update(configuration)
        self.name = name
        try:
            self._validate_configuration()
        except errors.ImproperlyConfigured as e:
            raise errors.ImproperlyConfigured('Command <{}> is improperly configured: {}'.format(self, e))

        logger.info('Registering command with configuration %s', self.configuration)
        # Parse regular expressions
        self.expressions = [re.compile(exp) for exp in self.configuration['expressions']]
        logger.info('Command <%s> will respond to the following expressions: %s', self.name, self.expressions)

    def _validate_configuration(self):
        return

    def understand(self, nervous_system, original_command, *commands):
        actions = self._understand(original_command, *commands)
        logger.debug(actions)
        for action in actions:
            logger.debug(action)
            action.publish(nervous_system)

    def _understand(self, original_command, *commands):
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

    def __str__(self):
        return self.name or self.__class__.__name__


class BlockingCommand(BaseCommand):

    def is_blocking_command(self):
        return True
