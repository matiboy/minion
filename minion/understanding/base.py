from . import operations
import re
import multiprocessing
import minion.understanding.exceptions
import minion.core.components
import minion.core.components.exceptions
import minion.core.utils.functions
import threading

logger = multiprocessing.get_logger()


class BaseCommand(minion.core.components.BaseComponent):
    configuration = {
        'action': 'noop',
        'expressions': []
    }
    multi = False
    threaded = False

    def __init__(self, name, configuration, preprocessors=[]):
        super(BaseCommand, self).__init__(name, configuration)
        logger.info('Registering command <%s> with configuration %s.', self.name, self._configuration)
        # TODO Add prefix?
        # Parse regular expressions
        self.expressions = [re.compile(exp) for exp in self.get_configuration('expressions', [])]
        if self.threaded:
            self.understand_runner = ThreadedUnderstandRunner()
        else:
            self.understand_runner = UnderstandRunner()
        logger.info('Command <%s> will respond to the following expressions: %s', self.name, ', '.join(map(lambda x: x.pattern, self.expressions)))

        processors = []
        for p in preprocessors:
            try:
                c = minion.core.utils.module_loading.import_string(p['class'])
            except ImportError:
                logger.critical('Unable to import {}'.format(p['class']))
            else:
                processors.append(c(p.get('configuration', {})))

        self.preprocessors = processors

    def understand(self, nervous_system, original_command, *commands):
        self.understand_runner.run(self, nervous_system, original_command, *commands)

    def _understand(self, original_command, *commands):
        raise NotImplementedError('"Understand" method must be implemented in command')

    def is_blocking_command(self):
        return False

    @minion.core.utils.functions.configuration_getter
    def get_action(self):
        return ''

    def get_command(self):
        """Deprecated: Should use get_action instead"""
        return self.get_configuration('action')

    def matches(self, command):
        commands = []

        for regular_expression in self.expressions:
            m = regular_expression.match(command)
            if m:
                if self.multi:
                    commands.append(m.groups())
                else:
                    return m.groups()
        if commands.__len__():
            return commands
        else:
            raise minion.understanding.exceptions.DoesNotMatch

    def __str__(self):
        return self.name or self.__class__.__name__


class RedirectCommand(BaseCommand):
    """
    A command type that does nothing but redirect input to corresponding output channel

    If unspecified on the class, the output is exactly equal to the input
    """
    def _get_output(self, original):
        try:
            return self.output
        except AttributeError:
            return original

    def _understand(self, original_command, *commands):
        return operations.UnderstandingOperation(self.get_action(), self._get_output(original_command))


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
            # Happens if the regular expression is somehow invalid
            raise minion.core.components.exceptions.ImproperlyConfigured('Parsed result command regular expression is invalid: {}'.format(e))

    def _match_command(self, command):
        matches = re.search(self.regular_expression, command)
        if matches is None:
            return None

        return matches.groupdict()

    def _understand(self, original_command, *commands):
        return (self._match_command(command) for command in commands)


class UnderstandRunner(object):
    def run(self, command_object, nervous_system, original_command, *commands):
        actions = command_object._understand(original_command, *commands)
        for action in actions:
            action.publish(nervous_system)


class ThreadedUnderstandRunner(UnderstandRunner):
    """
    Calls the same as Understand Runner exactly, but threaded
    """
    def run(self, *args):
        t = threading.Thread(target=super(ThreadedUnderstandRunner, self).run, args=args)
        t.start()
