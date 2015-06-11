from __future__ import absolute_import
import functools
import minion.acting.base
import minion.core.utils.functions
import minion.core.utils.console
import multiprocessing
import pigpio
import threading
import time

logger = multiprocessing.get_logger()


class GPIOActuator(minion.acting.base.BaseActuator):
    """
    Generic GPIO actuator using pigpio
    Child classes expect an instance of pigpiod to be running (likely as root)
    """
    def __init__(self, name, configuration, channels=[], **kwargs):
        super(GPIOActuator, self).__init__(name, configuration, channels, **kwargs)
        self.pi = self._setup_pi()
        self.pi.set_mode(self._get_pin(), pigpio.OUTPUT)

    def _setup_pi(self):
        return pigpio.pi()

    @minion.core.utils.functions.configuration_getter
    def _get_pin(self):
        return 14

    def high(self):
        self.pi.write(self._get_pin(), 1)

    def low(self):
        self.pi.write(self._get_pin(), 0)

    def wait(self, duration):
        time.sleep(float(duration))


class RunCommands(GPIOActuator):
    """
    Runs a series of commands provided as an array of strings in configuration "commands" property
    Choices of commands are taken from the parent class: high, low and wait
    In the case of wait, a duration can be passed after a ":" in the config.

    E.g:
    ```json
        {
            configuration: {
                commands: ["high", "wait:10", "low"]
            }
        }
    ```
    """
    @minion.core.utils.functions.configuration_getter
    def _get_commands(self):
        return []

    def _parse_command(self, command):
        """
        Expects a string (high, low, wait:5) and parses that to a method
        """
        method, _, extra = command.partition(':')
        # Let it raise and be handle by the calling method
        method = getattr(self, method)
        if extra:
            return functools.partial(method, extra)

        return method

    def act(self, *args, **kwargs):
        for x in self._get_commands():
            try:
                method = self._parse_command(x)
            except AttributeError:
                minion.core.utils.console.console_error('GPIO command <{}> does not exist'.format(x))
                continue

            try:
                # Make sure we didn't have a wrong number of arguments
                method()
            except TypeError as e:
                minion.core.utils.console.console_error('GPIO command <{}> has an invalid signature: {}'.format(x, e))


class OnThenOff(RunCommands):
    """
    Shortcut class for running GPIO commands high, wait then low
    """
    def _get_commands(self):
        return ['high', 'wait:{}'.format(self._get_delay()), 'low']

    @minion.core.utils.functions.configuration_getter
    def _get_delay(self):
        return 1.0

    def act(self, *args, **kwargs):
        # TODO Why is the threading handled at this particular level?
        t = threading.Thread(target=super(OnThenOff, self).act)
        t.start()


class OffThenOn(RunCommands):
    """
    Shortcut class for running GPIO commands low, wait then high
    """
    def _get_commands(self):
        return ['low', 'wait:{}'.format(self._get_delay()), 'high']

    @minion.core.utils.functions.configuration_getter
    def _get_delay(self):
        return 1.0

    def act(self, *args, **kwargs):
        # TODO Why is the threading handled at this particular level?
        t = threading.Thread(target=super(OffThenOn, self).act)
        t.start()
