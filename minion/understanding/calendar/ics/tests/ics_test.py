import unittest
from .. import ics
import mock
import minion.core.components.exceptions
import sure # though lint complains that it's never used this is needed


class ICSTodayConfiguration(unittest.TestCase):
    def test_no_resource(self):
        """Should raise if no url/path passed"""
        ics.IcsCalendarTodayEvents.when.called_with('somename', {}).should.throw(minion.core.components.exceptions.ImproperlyConfigured)

    def test_ok(self):
        """Should not raise if resource passed"""
        ics.IcsCalendarTodayEvents.when.called_with('somename', {'resource': 'a'}).should_not.throw(minion.core.components.exceptions.ImproperlyConfigured)


class ICSTomorrowConfiguration(unittest.TestCase):
    def test_no_resource(self):
        """Should raise if no url/path passed"""
        ics.IcsCalendarTomorrowEvents.when.called_with('somename', {}).should.throw(minion.core.components.exceptions.ImproperlyConfigured)

    def test_ok(self):
        """Should not raise if resource passed"""
        ics.IcsCalendarTomorrowEvents.when.called_with('somename', {'resource': 'a'}).should_not.throw(minion.core.components.exceptions.ImproperlyConfigured)


class IsUrlTest(unittest.TestCase):
    def test_is_url(self):
        calendar = ics.IcsCalendar('dsada', {'resource': 'http://www.google.com'})
        calendar._is_url().should.be.ok

    def test_is_url_https(self):
        calendar = ics.IcsCalendar('dsada', {'resource': 'https://somesite.com'})
        calendar._is_url().should.be.ok

    def test_is_not_url(self):
        calendar = ics.IcsCalendar('dsada', {'resource': '/home/user/lala.ics'})
        calendar._is_url().shouldnt.be.ok
