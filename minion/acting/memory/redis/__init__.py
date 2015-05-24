import minion.acting.base
import multiprocessing
import redis

logger = multiprocessing.get_logger()


class CommitToMemory(minion.acting.base.BaseActuator):
    configuration = {
        'host': 'localhost',
        'port': 6379,
        'db': 0,
        'separator': ' '
    }

    def __init__(self, name, configuration, channels=[], **kwargs):
        super(CommitToMemory, self).__init__(name, configuration, channels, **kwargs)
        redis_config = {x: self.get_configuration(x) for x in ['host', 'port', 'db']}
        self.redis_client = redis.StrictRedis(**redis_config)

    def get_separator(self):
        return self.get_configuration('separator')

    def act(self, message):
        try:
            # Wish I could use python 3's action, *rest = message.split
            all_stuff = message.split(self.get_separator())
            # Take the first as action, pass the rest
            action = all_stuff.pop(0)
            getattr(self, action)(*all_stuff)
        except ValueError:
            logger.error('An error occured while trying to parse commit to memory command %s', message)
        except AttributeError:
            logger.error('Commit to memory command not recognized %s (from message %s)', action, message)

    def set(self, key, value, *args):
        self.redis_client.set(key, value)

    def temporary(self, key, value, duration, *args):
        self.redis_client.setex(key, duration, value)
