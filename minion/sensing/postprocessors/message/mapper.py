import minion.sensing.postprocessors
import minion.sensing.exceptions
import minion.core.components.exceptions
import multiprocessing
import minion.core.utils.functions

logger = multiprocessing.get_logger()


class MapperPostprocessor(minion.sensing.postprocessors.BasePostprocessor):
    RAISE_KEYWORD = 'raise'
    @minion.core.utils.functions.configuration_getter
    def _get_default(self):
        return self.RAISE_KEYWORD

    @minion.core.utils.functions.configuration_getter
    def _get_map(self):
        return {}

    def process(self, data):
        mapper = self._get_map()

        if data in mapper:
            return mapper[data]

        if self._get_default() is self.RAISE_KEYWORD:
            raise minion.sensing.exceptions.DataUnavailable
        return self._get_default()
