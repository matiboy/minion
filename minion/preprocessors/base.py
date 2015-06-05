import minion.core.components
import minion.core.components.exceptions
import minion.core.utils.functions
from . import exceptions


class BasePreprocessor(minion.core.components.BaseComponent):
    configuration = {}
    blocking = False
    sufficient = False

    def __init__(self, configuration):
        # No need to name
        super(BasePreprocessor, self).__init__('', configuration)

    def test(self, *args, **kwargs):
        # TODO Not sure this is the right way to go
        # Allow to raise either on sufficient or blocking
        if self._test(*args, **kwargs):
            self.success()
        else:
            self.fail()
        return self._process(*args, **kwargs)


    def _process(self, *args, **kwargs):
        return args, kwargs

    def _test(self, *args, **kwargs):
        raise NotImplementedError('Test method needs to be implemented in preprocessor')

    @minion.core.utils.functions.configuration_getter
    def _get_blocking(self):
        # In case the value is set on the class not in the configuration
        return self.blocking

    @minion.core.utils.functions.configuration_getter
    def _get_sufficient(self):
        # In case the value is set on the class not in the configuration
        return self.sufficient

    def fail(self):
        if self._get_blocking():
            raise exceptions.StopProcess

    def success(self):
        if self._get_sufficient():
            raise exceptions.ProcessValid
