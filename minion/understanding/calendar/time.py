import minion.understanding.base
import minion.understanding.operations
import arrow
from dateutil import tz


class GiveMeTheTime(minion.understanding.base.BaseCommand):
    configuration = {
        'action': 'minion:speak',
        'expressions': ['^what time is it', "^what's the time", '^what is the time'],
        'time_format': 'h mm A'
    }

    def _understand(self, original_command, *commands):
        time = arrow.get(tz.tzlocal())

        return minion.understanding.operations.UnderstandingOperation(self.get_configuration('action'), time.format(self.get_configuration('time_format')))
