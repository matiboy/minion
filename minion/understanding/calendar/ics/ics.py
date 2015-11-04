from __future__ import absolute_import
import arrow
import ics
import minion.understanding.base
import minion.core.components.exceptions
import minion.core.utils.date
import requests
import urlparse


class LocalFileReader(object):
    def read(self, file_path):
        with open(file_path) as f:
            return f.read().decode('ISO-8859-1')


class UrlReader(object):
    def read(self, url):
        print url
        return requests.get(url).text


class IcsCalendar(minion.understanding.base.BaseCommand):
    configuration = {
        'action': 'minion:speak',
        'expressions': [],
    }
    threaded = True

    def _get_resource(self):
        return self.get_configuration('resource')

    def _is_url(self):
        as_url = urlparse.urlparse(self._get_resource())
        return as_url.scheme != ''

    def _validate_configuration(self):
        path_or_url = self._get_resource()

        if not path_or_url:
            raise minion.core.components.exceptions.ImproperlyConfigured('Resource url is needed')

        if self._is_url():
            self.reader = UrlReader()
        else:
            self.reader = LocalFileReader()

    def read(self):
        return self.reader.read(self._get_resource())

    def _events_to_messages(self, events):
        message = []
        for e in events:
            # TODO Look into all the cases
            begin = e.begin.to('local')
            start = minion.core.utils.date.easily_readable_time(begin)
            end = minion.core.utils.date.easily_readable_time(begin + e.duration)
            arguments = {
                'begin': start,
                'end': end,
                'name': e.name,
                'location': '',
            }
            if e.location:
                arguments['location'] = ' at {}'.format(e.location)

            message.append('{begin} to {end}. {name} {location}'.format(**arguments))

        return message


class IcsCalendarDayEvents(IcsCalendar):
    inbetween = '$$pause$$'

    def _get_events(self, calendar):
        return calendar.events.on(arrow.utcnow().replace(days=self.day))

    def _understand(self, original_command, *commands):
        calendar = ics.Calendar(self.read())

        # Make a copy since we use mutable methods
        message = list(self.prefix_message)

        # Defined in sub classes
        events = self._get_events(calendar)
        if events.__len__() == 0:
            message.append('No events')
        else:
            message.extend(self._events_to_messages(events))

        return minion.understanding.operations.UnderstandingOperation(self.get_command(), self.inbetween.join(message))


class IcsCalendarTodayEvents(IcsCalendarDayEvents):
    prefix_message = ['Events for today']
    day = 0


class IcsCalendarTomorrowEvents(IcsCalendarDayEvents):
    prefix_message = ['Events for tomorrow']
    day = 1
