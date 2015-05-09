import multiprocessing

logger = multiprocessing.get_logger()


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
