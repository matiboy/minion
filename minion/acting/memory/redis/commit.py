import minion.acting.base
import multiprocessing
import redis
import minion.core.utils.functions

logger = multiprocessing.get_logger()


class CommitToMemory(minion.acting.base.BaseActuator):
    def __init__(self, name, configuration, channels=[], **kwargs):
        super(CommitToMemory, self).__init__(name, configuration, channels, **kwargs)
        self.redis_client = self._setup_redis_client()

    def _setup_redis_client(self):
        return redis.StrictRedis(**self.get_redis())

    @minion.core.utils.functions.configuration_getter
    def get_redis(self):
        return {
            'host': 'localhost',
            'port': 6379,
            'db': 0
        }

    @minion.core.utils.functions.configuration_getter
    def get_separator(self):
        return ' '

    def act(self, message):
        try:
            # Wish I could use python 3's action, *rest = message.split
            all_stuff = message.split(self.get_separator())
            # Take the first as action, pass the rest
            action = all_stuff.pop(0)
            getattr(self, action)(*all_stuff)
        except IndexError:
            logger.error('Message is empty')
        except TypeError as e:
            print 'Error', e
            logger.error('Insufficient number of parts in message')
        except ValueError:
            logger.error('An error occured while trying to parse commit to memory command %s', message)
        except AttributeError:
            logger.error('Commit to memory command not recognized %s (from message %s)', action, message)

    def set(self, key, value, *args):
        self.redis_client.set(key, value)

    def temporary(self, key, value, duration, *args):
        self.redis_client.setex(key, duration, value)

    def forget(self, key, *args):
        self.redis_client.delete(key)
