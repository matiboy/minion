import minion.sensing.base
import multiprocessing

logger = multiprocessing.get_logger()


class Heartbeat(minion.sensing.base.ContinuousSensor):
    def sense(self):
        logger.debug('Heartbeat going to say something')
        return self.configuration['message']
