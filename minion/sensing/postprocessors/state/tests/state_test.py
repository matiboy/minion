import unittest
from .. import state
import minion.core.components.exceptions
import minion.sensing.exceptions
import sure # though lint complains that it's never used this is needed


class StateChange(unittest.TestCase):
    def setUp(self):
        self.pp = state.StateChange('dsadas', {})

    def test_no_change_dict(self):
        """Should raise DataUnavailable if no change"""
        self.pp.process({'a': 42, 'brainstorm': 5})
        self.pp.process.when.called_with({'brainstorm': 5, 'a': 42}).should.throw(minion.sensing.exceptions.DataUnavailable)

    def test_no_change_list(self):
        """Should raise DataUnavailable if no change"""
        self.pp.process([1, 2, 3, 4])
        self.pp.process.when.called_with([1, 2, 3, 4]).should.throw(minion.sensing.exceptions.DataUnavailable)

    def test_no_change_string(self):
        """Should raise DataUnavailable if no change"""
        self.pp.process('abcd')
        self.pp.process.when.called_with('abcd').should.throw(minion.sensing.exceptions.DataUnavailable)

    def test_no_change_int(self):
        """Should raise DataUnavailable if no change"""
        self.pp.process(5)
        self.pp.process.when.called_with(5).should.throw(minion.sensing.exceptions.DataUnavailable)

    def test_change_value_dict(self):
        """Should not raise DataUnavailable if a change has occured on one of the values"""
        self.pp.process({'a': 42, 'brainstorm': 5})
        self.pp.process.when.called_with({'brainstorm': 100, 'a': 42}).shouldnt.throw(minion.sensing.exceptions.DataUnavailable)

    def test_change_key_removed_dict(self):
        """Should not raise DataUnavailable if a key has been removed"""
        self.pp.process({'a': 42, 'brainstorm': 5})
        self.pp.process.when.called_with({'a': 42}).shouldnt.throw(minion.sensing.exceptions.DataUnavailable)

    def test_change_key_added_dict(self):
        """Should not raise DataUnavailable if a key has been added"""
        self.pp.process({'a': 42, 'brainstorm': 5})
        self.pp.process.when.called_with({'a': 42, 'brainstorm': 5, 'c': 100}).shouldnt.throw(minion.sensing.exceptions.DataUnavailable)

    def test_change_list_order(self):
        """Should not raise DataUnavailable if the order of the list has changed"""
        self.pp.process([1, 2, 3, 4])
        self.pp.process.when.called_with([4, 2, 3, 1]).shouldnt.throw(minion.sensing.exceptions.DataUnavailable)

    def test_change_list_add_item(self):
        """Should not raise DataUnavailable if an item has been added to the list"""
        self.pp.process([1, 2, 3, 4])
        self.pp.process.when.called_with([1, 2, 3, 4, 5]).shouldnt.throw(minion.sensing.exceptions.DataUnavailable)

    def test_change_list_modify_item(self):
        """Should not raise DataUnavailable if an item has been modified"""
        self.pp.process([1, 2, 3, 4])
        self.pp.process.when.called_with([1, 2, 3, 15]).shouldnt.throw(minion.sensing.exceptions.DataUnavailable)

    def test_change_list_remove_item(self):
        """Should not raise DataUnavailable if an item has been modified"""
        self.pp.process([1, 2, 3, 4])
        self.pp.process.when.called_with([1, 2, 3]).shouldnt.throw(minion.sensing.exceptions.DataUnavailable)

    def test_change_string(self):
        """Should not raise DataUnavailable string changed"""
        self.pp.process('abcd')
        self.pp.process.when.called_with('whatever').shouldnt.throw(minion.sensing.exceptions.DataUnavailable)

    def test_change_int(self):
        """Should not raise DataUnavailable changed int"""
        self.pp.process(5)
        self.pp.process.when.called_with(42).shouldnt.throw(minion.sensing.exceptions.DataUnavailable)


class StateEqualsConfiguration(unittest.TestCase):
    def test_no_value(self):
        """Should raise if no value is provided"""
        state.StateEquals.when.called_with('dsadas', {}).should.throw(minion.core.components.exceptions.ImproperlyConfigured)

    def test_ok(self):
        """Should not raise as long as a is provided, even an empty one"""
        state.StateEquals.when.called_with('dsadas', {'value': None}).shouldnt.throw(minion.core.components.exceptions.ImproperlyConfigured)


class StateEquals(unittest.TestCase):
    def setUp(self):
        self.pp = state.StateEquals('dsda', {'value': 1})

    def test_raises_on_not_value(self):
        """If value does not match, raise"""
        self.pp.process.when.called_with('fsd').should.throw(minion.sensing.exceptions.DataUnavailable)

    def test_goes_through_value(self):
        """If value matches, pass"""
        self.pp.process.when.called_with(1).shouldnt.throw(minion.sensing.exceptions.DataUnavailable)


class StateWithinConfiguration(unittest.TestCase):
    def test_no_values(self):
        """Should raise if no list of values is provided, or provided as something other than a list"""
        state.StateWithin.when.called_with('dsadas', {}).should.throw(minion.core.components.exceptions.ImproperlyConfigured)
        state.StateWithin.when.called_with('dsadas', {'values': {'a': 42}}).should.throw(minion.core.components.exceptions.ImproperlyConfigured)
        state.StateWithin.when.called_with('dsadas', {'values': 'harlo'}).should.throw(minion.core.components.exceptions.ImproperlyConfigured)

    def test_ok(self):
        """Should not raise as long as a list of values are provided"""
        state.StateWithin.when.called_with('dsadas', {'values': [1, 2, 3]}).shouldnt.throw(minion.core.components.exceptions.ImproperlyConfigured)


class StateWithin(unittest.TestCase):
    def setUp(self):
        self.pp = state.StateWithin('dsda', {'values': ['a', 'b', 'c']})

    def test_raises_if_invalid_data(self):
        """It should raise an unreadable data error if the data passed is anything besides a string, float, int or a list"""
        self.pp.process.when.called_with({}).should.throw(minion.sensing.exceptions.DataReadError)

    def test_raises_on_value_outside(self):
        """If any value outside authorized, raise"""
        self.pp.process.when.called_with('fsd').should.throw(minion.sensing.exceptions.DataUnavailable)
        self.pp.process.when.called_with(['a', 'd']).should.throw(minion.sensing.exceptions.DataUnavailable)

    def test_goes_through_value(self):
        """If all values are within, pass"""
        self.pp.process.when.called_with(['a', 'b']).shouldnt.throw(minion.sensing.exceptions.DataUnavailable)

    def test_goes_through_single_value(self):
        """If the value is within, pass"""
        self.pp.process.when.called_with('a').shouldnt.throw(minion.sensing.exceptions.DataUnavailable)
