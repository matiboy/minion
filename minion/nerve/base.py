import minion.core.components
import multiprocessing

logger = multiprocessing.get_logger()


class NervousMessage(object):
    message_type = 'message'

    def __init__(self, channel, message):
        self.channel = channel
        self.message = message

    def serialize(self):
        return self

    def deserialize(self):
        return self

    def get_message(self):
        return self.message

    def get_channel(self):
        return self.channel

    def __str__(self):
        return '{} | {}'.format(self.get_channel(), self.get_message())


class BaseNervousSystem(minion.core.components.BaseComponent):
    """
        Base nervous system class
        Nervous systems need to implement the listen and publish methods
    """

    def __init__(self, name, configuration={}, **kwargs):
        super(BaseNervousSystem, self).__init__(name, configuration)
        logger.info('Starting Nervous system <%s> with configuration %s', self.name, self._configuration)

    def listen(self):
        raise NotImplementedError

    def publish(self):
        raise NotImplementedError
