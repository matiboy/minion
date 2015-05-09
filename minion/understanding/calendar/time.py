import minion.understanding.base
import arrow
from dateutil import tz


class GiveMeTheTime(minion.understanding.base.BaseCommand):
    configuration = {
        'action': 'minion:speak',
        'expressions': [r'^what time is it']
    }

    def _understand(self, *commands):
        # Doesn't expect multi
        time = arrow.get(tz.tzlocal())

        return minion.understanding.base.UnderstandingCommand(self.configuration['action'], time.format('h mm a'))
