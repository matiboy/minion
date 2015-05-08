import multiprocessing

logger = multiprocessing.get_logger()


class BaseActuator(object):
    configuration = {}

    def __init__(self, name='', channels=[], configuration={}, **kwargs):
        self.configuration.update(configuration)
        self.name = name
        self.channels = channels
        logger.info('Actuator <%s> created with configuration %s. Able to handle channels %s', name, self.configuration, ', '.join(channels))

    def can_handle(self, channel, **kwargs):
        return channel in self.channels

    def act(self, *args, **kwargs):
        raise NotImplementedError('Act needs to be implemented in actuator')
