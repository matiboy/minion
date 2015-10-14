import minion.sensing.postprocessors
import minion.sensing.exceptions
import minion.core.components.exceptions
import multiprocessing
import minion.core.utils.functions
import math

logger = multiprocessing.get_logger()


class IntegerRounding(minion.sensing.postprocessors.BasePostprocessor):
    directions = {
        'nearest': round,
        'up': math.ceil,
        'down': math.floor
    }
    """
    Post processor to round a value
    """
    @minion.core.utils.functions.configuration_getter
    def _get_direction(self):
        return 'nearest'

    def process(self, data):
        # Make sure we can read the state as a float
        try:
            num = float(data)
        except ValueError:
            raise minion.sensing.exceptions.DataReadError('Unable to parse <{}> as a float'.format(data))

        # Apply
        func = self.directions[self._get_direction()]
        return int(func(num))
