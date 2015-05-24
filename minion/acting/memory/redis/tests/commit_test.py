from __future__ import absolute_import
import unittest
from .. import commit
import mock
import sure  # though lint complains that it's never used this is needed


class FakeRedisClient(object):
    """
        Helper class
        Avoids depending on having an actual redis server running during tests
    """
    def set(self, key, value):
        pass

    def setex(self, key, duration, value):
        pass

    def delete(self, key):
        pass

fake_redis_client = FakeRedisClient()


class RespondToActTestMethod(unittest.TestCase):
    """ Test actions depending on message """
    @mock.patch.object(commit.CommitToMemory, '_setup_redis_client', return_value=fake_redis_client)
    def test_set(self, *args):
        """ Should call set """
        actuator = commit.CommitToMemory('some name', {})

        with mock.patch.object(actuator, 'set') as s:
            actuator.act('set this that')
            s.assert_called_with('this', 'that')

    @mock.patch.object(commit.CommitToMemory, '_setup_redis_client', return_value=fake_redis_client)
    def test_temporary(self, *args):
        """ Should call temporary """
        actuator = commit.CommitToMemory('some name', {})

        with mock.patch.object(actuator, 'temporary') as s:
            actuator.act('temporary this that seconds')
            s.assert_called_with('this', 'that', 'seconds')

    @mock.patch.object(commit.CommitToMemory, '_setup_redis_client', return_value=fake_redis_client)
    def test_delete(self, *args):
        """ Should call forget """
        actuator = commit.CommitToMemory('some name', {})

        with mock.patch.object(actuator, 'forget') as s:
            actuator.act('forget lalala')
            s.assert_called_with('lalala')

    @mock.patch.object(commit.CommitToMemory, '_setup_redis_client', return_value=fake_redis_client)
    def test_temporary_too_short(self, *args):
        """ Should fail to call temporary """
        actuator = commit.CommitToMemory('some name', {})

        with mock.patch.object(commit.logger, 'error') as logger_error:
            actuator.act('temporary this that')
            logger_error.assert_called_with('Insufficient number of parts in message')

    @mock.patch.object(commit.CommitToMemory, '_setup_redis_client', return_value=fake_redis_client)
    def test_set_too_short(self, *args):
        """ Should fail to call set """
        actuator = commit.CommitToMemory('some name', {})

        with mock.patch.object(commit.logger, 'error') as logger_error:
            actuator.act('set this')
            logger_error.assert_called_with('Insufficient number of parts in message')

    @mock.patch.object(fake_redis_client, 'setex')
    @mock.patch.object(commit.CommitToMemory, '_setup_redis_client', return_value=fake_redis_client)
    def test_temporary_too_long(self, *args):
        """ Should call setex with only part of the text """
        actuator = commit.CommitToMemory('some name', {})
        actuator.act('temporary this that 200 something else')
        fake_redis_client.setex.assert_called_with('this', '200', 'that')

    @mock.patch.object(fake_redis_client, 'delete')
    @mock.patch.object(commit.CommitToMemory, '_setup_redis_client', return_value=fake_redis_client)
    def test_forget_too_long(self, *args):
        """ Should call delete with only part of the text """
        actuator = commit.CommitToMemory('some name', {})
        actuator.act('forget blop that 200 something else')
        fake_redis_client.delete.assert_called_with('blop')
