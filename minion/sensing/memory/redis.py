import arrow
import minion.core.components.exceptions
import minion.core.utils.functions
import minion.sensing.base
import multiprocessing
import redis

logger = multiprocessing.get_logger()


class Memcheck(minion.sensing.base.ContinuousSensor):
    configuration = {
        'redis_host': 'localhost',
        'redis_port': 6379,
        'redis_db': 0,
    }

    @minion.core.utils.functions.configuration_getter
    def _get_key(self):
        return ''

    def _validate_configuration(self):
        # Must have a non empty key
        if not self._get_key():
            raise minion.core.components.exceptions.ImproperlyConfigured('Sensor <{}> needs to contain a key')

    def __init__(self, name, nervous_system, configuration={}, preprocessors=[], postprocessors=[], **kwargs):
        super(Memcheck, self).__init__(name, nervous_system, configuration, preprocessors, postprocessors, **kwargs)
        self.redis_client = self._setup_redis()

    def _setup_redis(self):
        return redis.StrictRedis(**self.get_configuration_dict('redis_host', 'redis_port', 'redis_db'))

    def sense(self):
        now = arrow.utcnow().timestamp
        key = self._get_key()
        # Read commands
        commands = self.redis_client.zrangebyscore(key, 0, now)
        # Remove them from memory
        self.redis_client.zremrangebyscore(key, 0, now)
        # TODO How to handle several commands?
        if commands.__len__():
            return commands[0]
        # Means we're passing
        raise minion.sensing.exceptions.DataUnavailable
