from .. import base
import datetime
import minion.core.components.exceptions
import minion.core.utils.functions


def _get_now():
    """ Simply get now date time. Makes testing easier since datetime.datetime can't be mocked in python<3.5 """
    return datetime.datetime.now().time()


class ActiveBetweenTimes(base.BasePreprocessor):
    def __init__(self, configuration):
        super(ActiveBetweenTimes, self).__init__(configuration)

    @minion.core.utils.functions.configuration_getter
    def get_start_time(self):
        return None

    @minion.core.utils.functions.configuration_getter
    def get_end_time(self):
        return None

    def _validate_configuration(self):
        for key in ('start_time', 'end_time'):
            self.requires_configuration_key(key)
            self.requires_non_empty_configuration(key)
            # TODO: That's ugly but using a string works well with requires above
            t = getattr(self, 'get_{}'.format(key))()

            # Split at ':'
            hour, _, minute = t.partition(':')
            # Parse to numbers
            try:
                hour = int(hour)
                minute = int(minute)
            except ValueError:
                raise minion.core.components.exceptions.ImproperlyConfigured('"{}" is an invalid time'.format(t))

            setattr(self, key, datetime.time(hour, minute))

    def _test(self):
        now = _get_now()
        return now > self.start_time and now < self.end_time
