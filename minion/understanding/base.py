import re
import multiprocessing
import minion.core.components
import minion.core.components.exceptions

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


class BaseCommand(minion.core.components.BaseComponent):
    configuration = {
        'action': 'noop',
        'expressions': []
    }
    multi = False

    def __init__(self, name, configuration):
        super(BaseCommand, self).__init__(name, configuration)
        logger.info('Registering command <%s> with configuration %s.', self.name, self._configuration)
        # TODO Add prefix
        # Parse regular expressions
        self.expressions = [re.compile(exp) for exp in self.get_configuration('expressions')]
        logger.info('Command <%s> will respond to the following expressions: %s', self.name, self.expressions)

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

    def get_command(self):
        return self.get_configuration('action')

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


class ParsedResultCommand(BaseCommand):
    """
        A command that parses the results before attempting to decide on actions
    """
    def __init__(self, name, configuration):
        super(ParsedResultCommand, self).__init__(name, configuration)
        # Regexp flags
        try:
            flags = [getattr(re, x) for x in self.get_configuration('flags', [])]
        except AttributeError as e:
            raise minion.core.components.exceptions.ImproperlyConfigured('Invalid flag: {}'.format(e))

        try:
            reg_exp = self.get_configuration('regular_expression') or self.regular_expression
            self.regular_expression = re.compile(reg_exp, *flags)
        except AttributeError:
            # Will happen if regular expression config was left empty, and the class did not define a regex
            raise minion.core.components.exceptions.ImproperlyConfigured('Parsed result command requires either the class or the configuration to define a regular expression')
        except re.error as e:
            raise minion.core.components.exceptions.ImproperlyConfigured('Parsed result command regular expression is invalid: {}'.format(e))

    def _match_command(self, command):
        matches = re.match(self.regular_expression, command)
        if matches is None:
            return None

        return matches.groupdict()

    def _understand(self, original_command, *commands):
        return (self._match_command(command) for command in commands)


class BlockingCommand(BaseCommand):

    def is_blocking_command(self):
        return True
