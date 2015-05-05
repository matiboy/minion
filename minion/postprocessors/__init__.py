class BasePostprocessor(object):
    def __init__(self, configuration={}, **kwargs):
        if not hasattr(self, 'configuration'):
            self.configuration = {}
        self.configuration.update(configuration)
