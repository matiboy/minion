from __future__ import absolute_import
import unittest
from .. import intents
import mock
import minion.core.components.exceptions
import sure  # though lint complains that it's never used this is needed


class IntentEqualsPreprocessorConfiguration(unittest.TestCase):
    def test_no_value(self):
        """ Should raise if no value passed """
        intents.IntentEquals.when.called_with({}).should.throw(minion.core.components.exceptions.ImproperlyConfigured)

    def test_ok(self):
        """ Should not raise if all ok """
        intents.IntentEquals.when.called_with({'value': 10}).should_not.throw(minion.core.components.exceptions.ImproperlyConfigured)


class FakeRedisClient(object):
    """ Helper class """
    def __init__(self, value):
        self.value = value

    def get(self, key):
        return self.value


class IntentExistsTestMethod(unittest.TestCase):
    """ Test actual checks"""
    @mock.patch.object(intents.BaseIntent, '_setup_redis_client', return_value=FakeRedisClient(None))
    def test_does_not_exist(self, mock_redis_client):
        """ Should return false if getting returns none """
        pp = intents.IntentExists({})
        pp.test().should_not.be.ok

    @mock.patch.object(intents.BaseIntent, '_setup_redis_client', return_value=FakeRedisClient(1))
    def test_does_exists(self, mock_redis_client):
        """ Should return true if getting returns something """
        pp = intents.IntentExists({})
        pp.test().should.be.ok


class IntentDoesNotExistTestMethod(unittest.TestCase):
    """ Test actual checks"""
    @mock.patch.object(intents.BaseIntent, '_setup_redis_client', return_value=FakeRedisClient(None))
    def test_does_not_exist(self, mock_redis_client):
        """ Should return true if getting returns none """
        pp = intents.IntentDoesNotExist({})
        pp.test().should.be.ok

    @mock.patch.object(intents.BaseIntent, '_setup_redis_client', return_value=FakeRedisClient(1))
    def test_does_exists(self, mock_redis_client):
        """ Should return false if getting returns something """
        pp = intents.IntentDoesNotExist({})
        pp.test().should_not.be.ok


class IntentEqualsTestMethod(unittest.TestCase):
    """ Test actual checks"""
    @mock.patch.object(intents.BaseIntent, '_setup_redis_client', return_value=FakeRedisClient(None))
    def test_does_not_exist(self, mock_redis_client):
        """ Should return false if getting returns none """
        pp = intents.IntentEquals({'value': '1'})
        pp.test().should_not.be.ok

    @mock.patch.object(intents.BaseIntent, '_setup_redis_client', return_value=FakeRedisClient('2'))
    def test_wrong_value(self, mock_redis_client):
        """ Should return false if getting returns something else """
        pp = intents.IntentEquals({'value': '1'})
        pp.test().should_not.be.ok

    @mock.patch.object(intents.BaseIntent, '_setup_redis_client', return_value=FakeRedisClient('1'))
    def test_does_exists(self, mock_redis_client):
        """ Should return true if getting returns the same value """
        pp = intents.IntentEquals({'value': '1'})
        pp.test().should.be.ok
