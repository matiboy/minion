import unittest
from .. import date
import arrow
import datetime
import six
import sure


class HRDate(unittest.TestCase):
    def does_not_break_using_normal_datetime_test(self):
        """Datetime should be ok to pass as an argument, doesn't need to be Arrow"""
        now = datetime.datetime.now()
        if six.PY3:
            expected_type = 'unicode'
        else:
            expected_type = 'str'

        date.easily_readable_time(now).should.be.a(expected_type)

    def correct_output_afternoon_with_minutes_test(self):
        """Afternoon with minutes should be in format h mm A"""
        now = arrow.Arrow(2015, 6, 21, 13, 34, 10)

        date.easily_readable_time(now).should.be.equal('1 34 PM')

    def correct_output_morning_with_minutes_test(self):
        """Morning with minutes should be in format h mm A"""
        now = arrow.Arrow(2015, 6, 21, 5, 55, 20)

        date.easily_readable_time(now).should.be.equal('5 55 AM')

    def correct_output_morning_without_minutes_test(self):
        """Morning without minutes should be in format h A"""
        now = arrow.Arrow(2015, 6, 21, 6, 00, 20)

        date.easily_readable_time(now).should.be.equal('6 AM')
