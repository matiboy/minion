import minion.core.components
import minion.core.components.exceptions


class BasePreprocessor(minion.core.components.BaseComponent):
    configuration = {}

    def __init__(self, configuration):
        # No need to name
        super(BasePreprocessor, self).__init__('', configuration)

    def test(self):
        raise NotImplementedError('Test method needs to be implemented in preprocessor')
