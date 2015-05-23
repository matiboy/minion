import redis
from .. import base

class BaseIntent(base.BasePreprocessor):
    configuration = {
        'host': 'localhost',
        'port': 6379,
        'db': 0
    }

    def __init__(self, configuration):
        super(BaseIntent, self).__init__(configuration)
        self.redis_client = redis.StrictRedis(host=self.configuration['host'], port=self.configuration['port'], db=self.configuration['db'])


class IntentExists(BaseIntent):
    configuration = {
        'host': 'localhost',
        'port': 6379,
        'db': 0,
        'key': 'minion:asleep',
    }

    def test(self):
        return self.redis_client.get(self.configuration['key']) is not None


class IntentDoesNotExist(IntentExists):
    def test(self):
        return self.redis_client.get(self.configuration['key']) is None


class IntentEquals(BaseIntent):
    def test(self):
        return self.redis_client.get(self.configuration['key']) == self.configuration['value']
