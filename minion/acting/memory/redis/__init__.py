import minion.acting.base
import redis


class CommitToMemory(minion.acting.base.BaseActuator):
    configuration = {
        'host': 'localhost',
        'port': 6379,
        'db': 0,
    }

    def __init__(self, name, configuration, channels=[], **kwargs):
        super(CommitToMemory, self).__init__(name, configuration, channels, **kwargs)
        redis_config = {x: self.get_configuration(x) for x in ['host', 'port', 'db']}
        self.redis_client = redis.StrictRedis(**redis_config)


    def set(self, key, value):
        self.redis_client.set(key, value)
