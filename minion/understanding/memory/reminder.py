import minion.understanding.base
import minion.understanding.operations
import minion.core.utils.words_to_numbers
import minion.core.utils.date
import multiprocessing
import redis

logger = multiprocessing.get_logger()


def _timestamp(numbers, unit):
    return minion.core.utils.date.date_shift(numbers, unit).timestamp


class RemindMe(minion.understanding.base.ParsedResultCommand):
    configuration = {
        'redis': {
            'host': 'localhost',
            'port': 6379,
            'db': 0
        },
        'expressions': ['^remind me in (?P<to_be_parsed>.*)'],
        'future_command': 'say you asked me to remind you {what}',
        'confirmation_command': 'say sure, i will remind you in {numbers} {unit} {what}'
    }

    regular_expression = '(?P<numbers>.+)\s+(?P<unit>minutes?|seconds?|days?|weeks?)\s+(?P<what>.+)'

    def __init__(self, configuration={}, name=''):
        super(RemindMe, self).__init__(configuration, name)

        # Create redis client
        self.redis_client = redis.StrictRedis(**self.get_configuration('redis'))
        self.key = self.get_key()

    def get_key(self):
        return self.get_configuration('key')

    def _validate_configuration(self):
        # Fail if not set or empty
        if not self.get_key():
            raise minion.core.components.exceptions.ImproperlyConfigured('Key is required')

    def _understand(self, original_command, *commands):
        commands = super(RemindMe, self)._understand(original_command, *commands)
        exec_commands = []
        for as_dict in commands:
            # TODO Errors
            try:
                score = _timestamp(as_dict['numbers'], as_dict['unit'])
            except KeyError:
                logger.error('Unable to read expected data from %s', as_dict)
            except minion.core.utils.words_to_numbers.IllegalWordException:
                # Refer to minion.core.utils.words_to_numbers for list
                logger.error('Numbers do not appear to be valid')
            else:
                # Confirm
                confirm = self.get_configuration('confirmation_command')
                if confirm:
                    exec_commands.append(minion.understanding.operations.UnderstandingOperation(None, confirm.format(**as_dict)))
                # TODO serializing?
                self.redis_client.zadd(self.key, score, self.get_configuration('future_command').format(**as_dict))

        if exec_commands.__len__():
            return exec_commands
        return minion.understanding.operations.Noop()
