import minion.core.components
import minion.core.utils
import multiprocessing
import subprocess

logger = multiprocessing.get_logger()


class BaseActuator(minion.core.components.BaseComponent):
    """
        Base actuator class
        Sub classes need to implement the "act" method
    """
    configuration = {}

    def __init__(self, name, configuration, channels=[], preprocessors=[], **kwargs):
        super(BaseActuator, self).__init__(name, configuration)
        self.channels = channels
        logger.info('Actuator <%s> created with configuration %s. Able to handle channels %s', name, self._configuration, ', '.join(channels))

        processors = []
        for p in preprocessors:
            try:
                c = minion.core.utils.module_loading.import_string(p['class'])
            except ImportError:
                logger.critical('Unable to import {}'.format(p['class']))
            else:
                processors.append(c(p.get('configuration', {})))

        self.preprocessors = processors

    def can_handle(self, channel, **kwargs):
        return channel in self.channels

    def preprocess_then_act(self, *args, **kwargs):
        # Go through the preprocessors
        go_ahead = True
        for p in self.preprocessors:
            try:
                p.test()
            except minion.preprocessors.exceptions.StopProcess:
                go_ahead = False
                break
            except minion.preprocessors.exceptions.ProcessValid:
                # Means we can go ahead without checking other preprocessors
                break

        if go_ahead:
            self.act(*args, **kwargs)

    def act(self, *args, **kwargs):
        raise NotImplementedError('Act needs to be implemented in actuator')


class ShellCommandActuator(BaseActuator):
    """
        Actuator that will run a shell command using subprocess.
        Child classes need to implement _build_command which receives the same args and kwargs as BaseActuator's act

        Setting shell=True in child class is unsafe, see https://docs.python.org/2/library/subprocess.html#frequently-used-arguments
    """
    shell = False

    def _build_command(self, *args, **kwargs):
        """
            Returns a string or an array that will be passed to subprocess
        """
        raise NotImplementedError('Shell command actuator needs to implement build command')

    def act(self, *args, **kwargs):
        command = self._build_command(*args, **kwargs)
        exit_code = subprocess.call(command, shell=self.shell)
        if exit_code:
            logger.info('Command "%s" with shell set as %s exited with code %s', ' '.join(command), self.shell, exit_code)
