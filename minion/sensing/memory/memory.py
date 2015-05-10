import arrow
import minion.sensing.base
import minion.sensing.errors
import multiprocessing
import redis

logger = multiprocessing.get_logger()


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
        return self.configuration.get('key')

    def __init__(self, nervous_system, configuration={}, preprocessors=[], postprocessors=[], **kwargs):
        super(Memcheck, self).__init__(nervous_system, configuration, preprocessors, postprocessors, **kwargs)
        self.redis_client = redis.StrictRedis(**self.configuration['redis'])
        self.key = self.configuration['key']

    def sense(self):
        now = arrow.utcnow().timestamp
        commands = self.redis_client.zrangebyscore(self.key, 0, now)
        self.redis_client.zremrangebyscore(self.key, 0, now)
        # TODO How to handle several commands?
        if commands.__len__():
            return commands[0]
        raise minion.sensing.errors.DataUnavailable
