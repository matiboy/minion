import minion.sensing.base
import minion.core.components.exceptions
import minion.core.utils.functions
import multiprocessing

logger = multiprocessing.get_logger()


class Heartbeat(minion.sensing.base.ContinuousSensor):
    @minion.core.utils.functions.configuration_getter
    def _get_message(self):
        return ''

    def sense(self):
        logger.debug('Heartbeat going to say something')
        return self._get_message()

    def _validate_configuration(self):
        """Must have a non empty message"""
        if not self._get_message():
            raise minion.core.components.exceptions.ImproperlyConfigured('Sensor <{}> must have a non empty message'.format(self.name))
