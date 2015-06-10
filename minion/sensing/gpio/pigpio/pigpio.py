from __future__ import absolute_import
import minion.acting.base
import minion.core.utils.functions
import minion.core.utils.console
import multiprocessing
import pigpio

logger = multiprocessing.get_logger()


class Reader(minion.sensing.base.ContinuousSensor):
    period = 0.5
    """
    Generic GPIO sensor using pigpio
    Child classes expect an instance of pigpiod to be running (likely as root)
    """
    def __init__(self, name, nervous_system, configuration={}, preprocessors=[], postprocessors=[], **kwargs):
        super(Reader, self).__init__(name, nervous_system, configuration, preprocessors, postprocessors, **kwargs)
        self.pi = self._setup_pi()
        # Set the pin to input
        self.pi.set_mode(self._get_pin(), pigpio.INPUT)
        self.pi.set_pull_up_down(self._get_pin(), getattr(pigpio, self._get_pud()))

    def _setup_pi(self):
        return pigpio.pi()

    def get_publish_channel(self):
        return 'minion:proximity'

    @minion.core.utils.functions.configuration_getter
    def _get_pin(self):
        return 14

    @minion.core.utils.functions.configuration_getter
    def _get_pud(self):
        return 'PUD_OFF'

    def _validate_configuration(self):
        self.requires_configuration_key('pin')
        self.requires_non_empty_configuration('pin')

    def sense(self):
        # Always return, let the post processors decide what is what
        return self.pi.read(self._get_pin())
