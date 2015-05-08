from __future__ import absolute_import
from . import errors
import multiprocessing
import redis

logger = multiprocessing.get_logger()


class NervousSystem(object):
    configuration = {
        'host': 'localhost',
        'port': 6379,
        'db': 0
    }
    channel = 'minion:command'

    def __init__(self, configuration={}, **kwargs):
        self.configuration.update(configuration)
        logger.info('Starting Redis nervous system with configuration %s', self.configuration)
        self.redis_client = redis.StrictRedis(**self.configuration)
        try:
            self.redis_client.ping()
        except redis.ConnectionError:
            logger.critical('Unable to connect nervous system to Redis')
            raise errors.ImproperlyConfigured
        else:
            logger.info('Connection established to redis server {host}:{port} on db {db}'.format(**self.configuration))
        # Publishing channel
        if 'channel' in self.configuration:
            self.channel = self.configuration['channel']
        # If we have channels, means we are listening
        if 'channels' in kwargs:
            self.subscribing_redis_client = redis.StrictRedis(**self.configuration)
            self.channels = kwargs['channels']
            self.pubsub = self.subscribing_redis_client.pubsub()
            logger.info('Nervous system is now listening to channels %s', ', '.join(self.channels))
            self.pubsub.subscribe(*self.channels)

    def publish(self, channel=None, message=''):
        if not channel:
            channel = self.channel

        logger.debug('Nervous system publishing message %s on channel %s', message, channel)
        self.redis_client.publish(channel, message)

    def listen(self):
        return self.pubsub.listen()
