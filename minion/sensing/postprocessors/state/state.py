import minion.sensing.postprocessors
import minion.sensing.exceptions
import minion.core.components.exceptions
import multiprocessing
import minion.core.utils.functions

logger = multiprocessing.get_logger()


class StatePostprocessor(minion.sensing.postprocessors.BasePostprocessor):
    def __init__(self, name, configuration={}):
        super(StatePostprocessor, self).__init__(name, configuration)
        self.state = None

    def process(self, data):
        # Keep track of data
        old_state = self.state
        self.state = data
        return old_state, self.state


class StateChange(StatePostprocessor):
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
