import unittest
from .. import reminder

working_values = {
    'five minutes to boil eggs': {
        'numbers': 'five',
        'unit': 'minutes',
        'what': 'to boil eggs'
    },
    'twenty two seconds to boil eggs': {
        'numbers': 'twenty two',
        'unit': 'seconds',
        'what': 'to boil eggs'
    },
    'twenty two second to boil eggs': {
        'numbers': 'twenty two',
        'unit': 'second',
        'what': 'to boil eggs'
    },
}

class StringParsingTest(unittest.TestCase):
    def test_parsing(self):
        for string, result in working_values.iteritems():
            actual_result = reminder._parse(string).groupdict()
            for group_name, value in actual_result.iteritems():
                print group_name, result[group_name], value
                assert result[group_name] == value

class DateParsing(unittest.TestCase):
    def test_parsing(self):
        # TODO Write those tests using mock
        print reminder._timestamp('five', 'minutes')
        print reminder._timestamp('twenty', 'minute')
        assert False is True