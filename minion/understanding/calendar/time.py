import minion.understanding.base
import arrow
from dateutil import tz


class GiveMeTheTime(minion.understanding.base.BaseCommand):
    configuration = {
        'action': 'minion:speak',
        'expressions': ['^what time is it', "^what's the time", '^what is the time'],
        'time_format': 'h mm A'
    }

    def _understand(self, original_command, *commands):
        # Doesn't expect multi
        time = arrow.get(tz.tzlocal())

        return minion.understanding.base.UnderstandingCommand(self.configuration['action'], time.format(self.configuration['time_format']))
