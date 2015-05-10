import minion.understanding.base
import minion.understanding.errors
import minion.utils.words_to_numbers
import multiprocessing
import redis
import re
import arrow

logger = multiprocessing.get_logger()


def _parse(to_be_parsed):
    exp = re.compile('(?P<numbers>.+)\s+(?P<unit>minutes?|seconds?|days?|weeks?)\s+(?P<what>.+)')
    return exp.match(to_be_parsed)

def _timestamp(numbers, unit):
    return _date_shift(numbers, unit).timestamp

def _date_shift(numbers, unit):
    now = arrow.utcnow()

    if unit[-1] != 's':
        unit = unit + 's'

    kwargs = {
        unit: minion.utils.words_to_numbers.text2int( numbers )
    }

    after_shift = now.replace(**kwargs)

    return after_shift


class RemindMe(minion.understanding.base.BaseCommand):
    configuration = {
        'redis': {
            'host': 'localhost',
            'port': 6379,
            'db': 0
        },
        'expressions': [r'^remind me in (?P<to_be_parsed>.*)'],
        'future_command': 'say you asked me to remind you {}'
    }

    def __init__(self, configuration={}, name=''):
        super(RemindMe, self).__init__(configuration, name)

        # Create redis client
        self.redis_client = redis.StrictRedis(**self.configuration['redis'])
        self.key = self.configuration['key']

    def _validate_configuration(self):
        # Fail if not set or empty
        if not self.configuration.get('key'):
            raise minion.understanding.errors.ImproperlyConfigured('Key is required')

    def _understand(self, original_command, *commands):
        command = commands[0]
        logger.debug(command)
        matches = _parse(command)
        logger.debug(matches)
        if matches:
            as_dict = matches.groupdict()

            # TODO Errors
            score = _timestamp(as_dict['numbers'], as_dict['unit'])

            # TODO serializing
            self.redis_client.zadd(self.key, score, self.configuration['future_command'].format(as_dict['what']))

        return minion.understanding.base.Noop()
