from .. import base
import datetime
import minion.core.components.exceptions


def _get_now(self):
    """ Simply get now date time. Makes testing easier since datetime.datetime can't be mocked in python<3.5 """
    return datetime.datetime.now().time()


class ActiveBetweenTimes(base.BasePreprocessor):
    def __init__(self, configuration):
        super(ActiveBetweenTimes, self).__init__(configuration)

    def _validate_configuration(self):
        for key in ('start_time', 'end_time'):
            t = self.get_configuration(key)
            # Make sure we have a config value
            if not t:
                raise minion.core.components.exceptions.ImproperlyConfigured('<{}> is required'.format(key))

            # Split at ':'
            hour, _, minute = t.partition(':')
            # Parse to numbers
            try:
                hour = int(hour)
                minute = int(minute)
            except ValueError:
                raise minion.core.components.exceptions.ImproperlyConfigured('"{}" is an invalid time'.format(t))

            setattr(self, key, datetime.time(hour, minute))

    def test(self):
        now = _get_now()
        return now > self.start_time and now < self.end_time
