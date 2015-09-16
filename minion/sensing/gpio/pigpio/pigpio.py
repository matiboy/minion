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

class MCP3008Reader(minion.sensing.base.ContinuousSensor):
    period = 1

    """
    GPIO sensor for MCP3008 analog using pigpio
    Child classes expect an instance of pigpiod to be running (likely as root)
    """
    def __init__(self, name, nervous_system, configuration={}, preprocessors=[], postprocessors=[], **kwargs):
        super(Reader, self).__init__(name, nervous_system, configuration, preprocessors, postprocessors, **kwargs)
        self.pi = self._setup_pi()
        # Set the pin to input
        self.pi.set_mode(self._get_spimiso(), pigpio.INPUT)
        self.pi.set_mode(self._get_spimosi(), pigpio.OUTPUT)
        self.pi.set_mode(self._get_spics(), pigpio.OUTPUT)
        self.pi.set_mode(self._get_spiclk(), pigpio.OUTPUT)

    def _setup_pi(self):
        return pigpio.pi()

    @minion.core.utils.functions.configuration_getter
    def _get_channel(self):
        return 0

    @minion.core.utils.functions.configuration_getter
    def _get_spiclk(self):
        return 18

    @minion.core.utils.functions.configuration_getter
    def _get_spimiso(self):
        return 23

    @minion.core.utils.functions.configuration_getter
    def _get_spimosi(self):
        return 24

    @minion.core.utils.functions.configuration_getter
    def _get_spics(self):
        return 25

    def sense(self):
        # Always return, let the post processors decide what is what
        return readadc(self.pi, self._get_channel(), self._get_spiclk(), self._get_spimosi(), self._get_spimiso(), self._get_spics())

# Helper function
def readadc(pi, adcnum, clockpin, mosipin, misopin, cspin):
    if ((adcnum > 7) or (adcnum < 0)):
        return -1

    pi.write(cspin, pigpio.HIGH)
    pi.write(clockpin, pigpio.LOW)
    pi.write(cspin, pigpio.LOW)

    commandout = adcnum
    commandout |= 0x18  # start bit + single-ended bit
    commandout <<= 3    # we only need to send 5 bits here
    for i in range(5):
        if (commandout & 0x80):
            pi.write(mosipin, pigpio.HIGH)
        else:
            pi.write(mosipin, pigpio.LOW)
        commandout <<= 1
        pi.write(clockpin, pigpio.HIGH)
        pi.write(clockpin, pigpio.LOW)

    adcout = 0
    # read in one empty bit, one null bit and 10 ADC bits
    for i in range(12):
        pi.write(clockpin, pigpio.HIGH)
        pi.write(clockpin, pigpio.LOW)
        adcout <<= 1

        if pi.read(misopin) == pigpio.HIGH:
            adcout |= 0x1

    pi.write(cspin, pigpio.HIGH)

    adcout >>= 1       # first bit is 'null' so drop it
    return adcout
