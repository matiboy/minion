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


class BaseNervousSystem(object):
    configuration = {}

    def __init__(self, configuration={}, **kwargs):
        self.configuration = self.configuration.copy()
        self.configuration.update(configuration)

        logger.info('Starting Nervous system with configuration %s', self.configuration)

    def listen(self):
        raise NotImplementedError

    def publish(self):
        raise NotImplementedError
