import minion.sensing.postprocessors
import minion.sensing.exceptions
import minion.core.components.exceptions
import multiprocessing
import minion.core.utils.functions
import six

logger = multiprocessing.get_logger()


class StatePostprocessor(minion.sensing.postprocessors.BasePostprocessor):
    """
    Abstract postprocessor to keep state from one process call to the next
    """
    def __init__(self, name, configuration={}):
        super(StatePostprocessor, self).__init__(name, configuration)
        self.state = None

    def process(self, data):
        # Keep track of data
        old_state = self.state
        self.state = data
        return old_state, self.state


class StateChange(StatePostprocessor):
    """
    Post processor that only lets data through if it has changed from the previous time process was called. Keeps its state internally
    """
    def has_changed(self, old):
        """
        Compares the old and new states
        At this moment it is a straight forward comparison on primitives but we might implement something else in the future
        """
        return old != self.state

    def process(self, data):
        old_state, new_state = super(StateChange, self).process(data)

        # Compare the various types of data
        # TODO this is a good example why we should probably abstract the data objects into several classes which need to implement a comparison method
        has_changed = self.has_changed(old_state)

        if not has_changed:
            raise minion.sensing.exceptions.DataUnavailable
        else:
            return data


class StateEquals(StatePostprocessor):
    """
    Post processor that checks that the data provided for processing is equal to the value provided at configuration level
    """
    @minion.core.utils.functions.configuration_getter
    def _get_value(self):
        return None

    def _validate_configuration(self):
        self.requires_configuration_key('value')

    def process(self, data):
        super(StateEquals, self).process(data)

        # Check whether state is equal to provided value
        if data != self._get_value():
            raise minion.sensing.exceptions.DataUnavailable

        return data


class StateWithin(StatePostprocessor):
    """
    Post processor that checks that all values provided for processing are within a list provided at configuration level
    """
    ACCEPTABLE_TYPES = tuple([int, float, list] + list(six.string_types))

    @minion.core.utils.functions.configuration_getter
    def _get_values(self):
        return []

    def _validate_configuration(self):
        self.requires_configuration_key('values')
        if not isinstance(self._get_values(), list):
            raise minion.core.components.exceptions.ImproperlyConfigured('Values should be a list, got {}'.format(type(self._get_values())))

    def process(self, data):
        super(StateWithin, self).process(data)
        values = self._get_values()

        if not isinstance(data, self.ACCEPTABLE_TYPES):
            raise minion.sensing.exceptions.DataReadError('Invalid data type <{}>'.format(type(data)))

        # Special for list, all items need to be within the values providded
        if isinstance(data, list):
            ok = all(x in values for x in data)

        else:
            ok = data in values

        if not ok:
            raise minion.sensing.exceptions.DataUnavailable
        return data
