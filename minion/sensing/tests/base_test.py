import unittest
from .. import base
from .. import exceptions
import mock
import minion.core.components.class_validation
import minion.core.components.exceptions
import sure # though lint complains that it's never used this is needed
import time


class ContinuousSensorPeriods(unittest.TestCase):
    def test_nothing_passed(self):
        """Should return 0 as period if nothing in config or on class"""
        with mock.patch.object(minion.core.components.class_validation, 'is_nervous_system') as i:
            i.return_value = True
            sensor = base.ContinuousSensor('dsada', None, {})
            sensor._get_period().should.equal(0)

    def test_config_passed(self):
        """Should return what is in the config"""
        with mock.patch.object(minion.core.components.class_validation, 'is_nervous_system') as i:
            i.return_value = True
            sensor = base.ContinuousSensor('dsada', None, {'period': 2})
            sensor._get_period().should.equal(2)

    def test_active_period(self):
        """Should the value itself or the first element of a period list"""
        with mock.patch.object(minion.core.components.class_validation, 'is_nervous_system') as i:
            i.return_value = True
            sensor = base.ContinuousSensor('dsada', None, {'period': 5})
            sensor._get_active_period().should.equal(float(5))
            sensor = base.ContinuousSensor('dsada', None, {'period': (1, 4)})
            sensor._get_active_period().should.equal(float(1))

    def test_inactive_period(self):
        """Should the second element of a period list or the value itself if not a list"""
        with mock.patch.object(minion.core.components.class_validation, 'is_nervous_system') as i:
            i.return_value = True
            sensor = base.ContinuousSensor('dsada', None, {'period': 5})
            sensor._get_inactive_period().should.equal(float(5))
            sensor = base.ContinuousSensor('dsada', None, {'period': (1, 4)})
            sensor._get_inactive_period().should.equal(float(4))

    def test_inactive_period_used_if_inactive(self):
        """Should the second element of a period list or the value itself if not a list"""
        with mock.patch.object(minion.core.components.class_validation, 'is_nervous_system') as i:
            i.return_value = True
            sensor = base.ContinuousSensor('dsada', None, {'period': 5, 'immediate': False})
            # Mock some stuff to fit what we need
            sensor.is_active = mock.Mock(return_value=False)
            sensor.sense = mock.Mock(side_effect=exceptions.DataUnavailable)
            with mock.patch.object(time, 'sleep') as timeSleep:
                # Make it raise so it stops the loop
                timeSleep.side_effect = Exception
                try:
                    sensor.run()
                except:
                    timeSleep.assert_called_with(float(5))
            sensor = base.ContinuousSensor('dsada', None, {'period': (10,20), 'immediate': False})
            # Mock some stuff to fit what we need
            sensor.is_active = mock.Mock(return_value=False)
            sensor.sense = mock.Mock(side_effect=exceptions.DataUnavailable)
            with mock.patch.object(time, 'sleep') as timeSleep:
                # Make it raise so it stops the loop
                timeSleep.side_effect = Exception
                try:
                    sensor.run()
                except:
                    timeSleep.assert_called_with(float(20))
