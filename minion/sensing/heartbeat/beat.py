import minion.sensing.base
import minion.core.components.exceptions
import multiprocessing

logger = multiprocessing.get_logger()


class Heartbeat(minion.sensing.base.ContinuousSensor):
    message_key = 'message'

    def sense(self):
        logger.debug('Heartbeat going to say something')
        return self.get_configuration(self.message_key)

    def _validate_configuration(self):
        """Must have a non empty message"""
        if not self.get_configuration(self.message_key):
            raise minion.core.components.exceptions.ImproperlyConfigured('Sensor <{}> must have a non empty "{}" configuration value'.format(self.name, self.message_key))
