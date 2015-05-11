import arrow
import minion.core.components.exceptions
import minion.sensing.base
import multiprocessing
import redis

logger = multiprocessing.get_logger()

KEY = 'key'

class Memcheck(minion.sensing.base.ContinuousSensor):
    configuration = {
        'redis': {
            'host': 'localhost',
            'port': 6379,
            'db': 0
        },
    }
    period = 1

    def _validate_configuration(self):
        # Must have a non empty key
        if not self.get_configuration(KEY):
            raise minion.core.components.exceptions.ImproperlyConfigured('Sensor <{}> needs to contain a ')

    def __init__(self, name, nervous_system, configuration={}, preprocessors=[], postprocessors=[], **kwargs):
        super(Memcheck, self).__init__(name, nervous_system, configuration, preprocessors, postprocessors, **kwargs)
        self.redis_client = redis.StrictRedis(**self.get_configuration('redis'))
        self.key = self.get_configuration(KEY)

    def sense(self):
        now = arrow.utcnow().timestamp
        # Read commands
        commands = self.redis_client.zrangebyscore(self.key, 0, now)
        # Remove them from memory
        self.redis_client.zremrangebyscore(self.key, 0, now)
        # TODO How to handle several commands?
        if commands.__len__():
            return commands[0]
        # Means we're passing
        raise minion.sensing.exceptions.DataUnavailable
