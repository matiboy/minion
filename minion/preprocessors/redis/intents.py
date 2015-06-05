import redis
from .. import base
import minion.core.components.exceptions
import minion.core.utils.functions

class BaseIntent(base.BasePreprocessor):
    """
        Base redis intent
        configuration should always be valid since we only update the class config
    """
    configuration = {
        'host': 'localhost',
        'port': 6379,
        'db': 0
    }

    def __init__(self, configuration):
        super(BaseIntent, self).__init__(configuration)
        self.redis_client = self._setup_redis_client()

    def _setup_redis_client(self):
        """ Creates the redis client according to configuration """
        return redis.StrictRedis(self.get_configuration_dict('host', 'port', 'db'))


class KeyBasedIntent(BaseIntent):
    """ Adds a get_key method for further sub classes that need to get a single redis key """
    @minion.core.utils.functions.configuration_getter
    def get_key(self):
        return None


class IntentExists(KeyBasedIntent):
    configuration = {
        'host': 'localhost',
        'port': 6379,
        'db': 0
    }

    blocking = True

    def _validate_configuration(self):
        if not self.get_key():
            raise minion.core.components.exceptions.ImproperlyConfigured('Key is required')

    def _test(self, *args, **kwargs):
        return self.redis_client.get(self.get_key())


class IntentDoesNotExist(IntentExists):
    """
        Checks that the given key does _not_ exist in the redis client
    """
    def _test(self):
        return self.redis_client.get(self.get_key()) is None


class IntentEquals(KeyBasedIntent):
    """
        Checks that the given key is equal to the given (constant) value
    """
    @minion.core.utils.functions.configuration_getter
    def get_value(self):
        return None

    def _validate_configuration(self):
        if not self.get_value():
            raise minion.core.components.exceptions.ImproperlyConfigured('Value is required for IntentEquals preprocessor')

    def _test(self):
        return self.redis_client.get(self.get_key()) == self.get_value()
