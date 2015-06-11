from __future__ import absolute_import
import unittest
from .. import timer
import mock
import minion.core.components.exceptions
import datetime
import sure # though lint complains that it's never used this is needed


class TimerPreprocessorConfiguration(unittest.TestCase):
    def test_no_start_time(self):
        """Should raise if no start time passed"""
        timer.ActiveBetweenTimes.when.called_with({}).should.throw(minion.core.components.exceptions.ImproperlyConfigured)

    def test_valid_start_time(self):
        """Should raise if invalid start time passed"""
        timer.ActiveBetweenTimes.when.called_with({'start_time': 'something without a colon'}).should.throw(minion.core.components.exceptions.ImproperlyConfigured)

    def test_valid_start_time2(self):
        """Should raise if invalid start time passed"""
        timer.ActiveBetweenTimes.when.called_with({'start_time': '8:blop'}).should.throw(minion.core.components.exceptions.ImproperlyConfigured)

    def test_no_end_time(self):
        """Should raise if no end time passed"""
        timer.ActiveBetweenTimes.when.called_with({'start_time': '8:00'}).should.throw(minion.core.components.exceptions.ImproperlyConfigured)

    def test_valid_end_time(self):
        """Should raise if invalid end time passed"""
        timer.ActiveBetweenTimes.when.called_with({'start_time': '8:00', 'end_time': 'something'}).should.throw(minion.core.components.exceptions.ImproperlyConfigured)

    def test_valid_end_time2(self):
        """Should raise if invalid end time passed"""
        timer.ActiveBetweenTimes.when.called_with({'start_time': '8:00', 'end_time': 'some:00'}).should.throw(minion.core.components.exceptions.ImproperlyConfigured)

    def test_ok(self):
        """Should not raise if all ok"""
        timer.ActiveBetweenTimes.when.called_with({'start_time': '8:00', 'end_time': '20:00'}).should_not.throw(minion.core.components.exceptions.ImproperlyConfigured)


@mock.patch('minion.preprocessors.timer.timer._get_now', return_value=datetime.time(10, 20))
class TimePreprocessorTestMethod(unittest.TestCase):
    """ Test actual checks"""
    def test_earlier_than_start(self, mock_get_now):
        """ Should return false if start is after now """
        pp = timer.ActiveBetweenTimes({'start_time': '11:00', 'end_time': '20:00'})
        pp._test().should_not.be.ok

    def test_later_than_end(self, mock_get_now):
        """ Should return false if end is before now """
        pp = timer.ActiveBetweenTimes({'start_time': '5:00', 'end_time': '10:00'})
        pp._test().should_not.be.ok

    def test_within_range(self, mock_get_now):
        """ Should return false if end is before now """
        pp = timer.ActiveBetweenTimes({'start_time': '10:00', 'end_time': '13:00'})
        pp._test().should.be.ok
