import minion.sensing.postprocessors
import minion.sensing.exceptions
import minion.core.components.exceptions
import multiprocessing
import minion.core.utils.functions

logger = multiprocessing.get_logger()


class LinearPostprocessor(minion.sensing.postprocessors.BasePostprocessor):
    """
    Post processor to transform a value into another using a linear function
    Configuration simply requires the values of a and b in y = ax + b
    """
    @minion.core.utils.functions.configuration_getter
    def _get_a(self):
        return 1

    @minion.core.utils.functions.configuration_getter
    def _get_b(self):
        return 0

    def process(self, data):
        # Make sure we can read the state as a float
        try:
            num = float(data)
        except ValueError:
            raise minion.sensing.exceptions.DataReadError('Unable to parse <{}> as a float'.format(data))

        # Apply
        return (self._get_a() * num) + self._get_b()
