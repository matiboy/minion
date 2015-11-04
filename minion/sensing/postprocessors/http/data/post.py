import minion.sensing.postprocessors
import minion.sensing.exceptions
import minion.core.components.exceptions
import minion.core.utils.functions
import multiprocessing

logger = multiprocessing.get_logger()


class PostDataPostProcessor(minion.sensing.postprocessors.BasePostprocessor):
    @minion.core.utils.functions.configuration_getter
    def _get_key(self):
        return 'message'

    @minion.core.utils.functions.configuration_getter
    def _get_passthrough(self):
        return False

    def process(self, data):
        """
            Data comes in as a MultiDict. Out as the post data value that corresponds to the key
        """
        if data.get(self._get_key()):
            return data.get(self._get_key())

        if not self._get_passthrough():
            return None

        return data
