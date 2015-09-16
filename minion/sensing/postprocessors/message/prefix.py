import minion.sensing.postprocessors
import minion.sensing.exceptions
import minion.core.components.exceptions
import minion.core.utils.functions


class PrefixAdder(minion.sensing.postprocessors.BasePostprocessor):
    """
    Post processor to add a prefix to the value
    """
    @minion.core.utils.functions.configuration_getter
    def _get_prefix(self):
        return None

    def _validate_configuration(self):
        self.requires_configuration_key('prefix')
        self.requires_non_empty_configuration('prefix')

    def process(self, data):
        return '{prefix}{message}'.format(prefix=self._get_prefix(), message=data)
