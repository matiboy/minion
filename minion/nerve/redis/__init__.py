import redis

class Redis(object):
    configuration = {
        'host': 'localhost',
        'port': 6379,
        'db': 0
    }
    channel = 'command'

    def __init__(self, configuration={}, **kwargs):
        self.configuration.update(configuration)
        self.redis_client = redis.StrictRedis(**self.configuration)
        self.subscribing_redis_client = redis.StrictRedis(**self.configuration)
        if 'channel' in configuration:
            self.channel = configuration['channel']

    def publish(self, channel=None, message=''):
        if not channel:
            channel = self.channel

        self.redis_client.publish(channel, message)
