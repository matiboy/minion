import minion.core.components
import multiprocessing
import subprocess

logger = multiprocessing.get_logger()


class BaseActuator(minion.core.components.BaseComponent):
    """
        Base actuator class
        Sub classes need to implement the "act" method
    """
    configuration = {}

    def __init__(self, name, configuration, channels=[], **kwargs):
        super(BaseActuator, self).__init__(name, configuration)
        self.channels = channels
        logger.info('Actuator <%s> created with configuration %s. Able to handle channels %s', name, self._configuration, ', '.join(channels))

    def can_handle(self, channel, **kwargs):
        return channel in self.channels

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
