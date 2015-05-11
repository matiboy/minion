import minion.core.components
import multiprocessing

logger = multiprocessing.get_logger()


class BaseActuator(minion.core.components.BaseComponent):
    configuration = {}

    def __init__(self, name, configuration, channels=[], **kwargs):
        super(BaseActuator, self).__init__(name, configuration)
        self.channels = channels
        logger.info('Actuator <%s> created with configuration %s. Able to handle channels %s', name, self._configuration, ', '.join(channels))

    def can_handle(self, channel, **kwargs):
        return channel in self.channels

    def act(self, *args, **kwargs):
        raise NotImplementedError('Act needs to be implemented in actuator')
