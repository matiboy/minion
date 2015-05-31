import minion.acting.base
import minion.core.utils.functions
import multiprocessing
import pigpio
import threading
import time

logger = multiprocessing.get_logger()


class OnThenOff(minion.acting.base.BaseActuator):
    @minion.core.utils.functions.configuration_getter
    def _get_pin(self):
        return 14

    @minion.core.utils.functions.configuration_getter
    def _get_delay(self):
        return 1.0

    def _turn_on_then_off(self):
        pi = pigpio.pi()
        pi.write(self._get_pin(), 1)
        time.sleep(self._get_delay())
        pi.write(self._get_pin(), 0)

    def act(self, *args, **kwargs):
        t = threading.Thread(target=self._turn_on_then_off)
        t.start()
