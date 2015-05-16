from __future__ import absolute_import
from . import errors
from . import base
import multiprocessing
import redis
import itertools

logger = multiprocessing.get_logger()


def remove_non_messages(x):
    return x['type'] == 'message'


def make_message_object(x):
    """
        Maps a redis message to a nervous message
    """
    return base.NervousMessage(x['channel'], x['data'])


class NervousSystem(base.BaseNervousSystem):
    configuration = {
        'host': 'localhost',
        'port': 6379,
        'db': 0
    }
    # Publishing channel
    channel = 'minion:command'

    def __init__(self, name, configuration, **kwargs):
        super(NervousSystem, self).__init__(name, configuration)

        self.redis_client = redis.StrictRedis(**self._configuration)

        try:
            self.redis_client.ping()
        except redis.ConnectionError:
            logger.critical('Unable to connect nervous system to Redis')
            raise errors.ImproperlyConfigured
        else:
            logger.info('Connection established to redis server {host}:{port} on db {db}'.format(**self._configuration))

        # Publishing channel   found in config or default to class channel
        self.channel = self.get_configuration('command_channel', self.channel)

    def publish(self, channel=None, message=''):
        if not channel:
            channel = self.channel

        logger.debug('Nervous system publishing message %s on channel %s', message, channel)
        self.redis_client.publish(channel, message)

    def listen(self):
        from_redis = self.pubsub.listen()
        # Remove non messages
        messages_only = itertools.ifilter(remove_non_messages, from_redis)
        # Map to message objects
        return itertools.imap(make_message_object, messages_only)

    def subscribe(self, *channels):
        logger.debug(channels)
        subscribing_redis_client = redis.StrictRedis(**self._configuration)
        self.pubsub = subscribing_redis_client.pubsub()
        self.pubsub.subscribe(*channels)
        logger.info('Nervous system is now listening to channels %s', ', '.join(channels))
