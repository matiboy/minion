class BasePreprocessor(object):
    configuration = {}

    def __init__(self, configuration):
        self.configuration = self.configuration.copy()
        self.configuration.update(configuration)

    def test(self):
        raise NotImplementedError('Test method needs to be implemented in preprocessor')