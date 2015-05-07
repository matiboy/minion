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
        self.subscribing_redis_client = redis.StrictRedis(**self.configuration)
        if 'channel' in configuration:
            self.channel = configuration['channel']

    def publish(self, channel=None, message=''):
        if not channel:
            channel = self.channel

        logger.debug('Nervous system publishing message %s on channel %s', message, channel)
        self.redis_client.publish(channel, message)
