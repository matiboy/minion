from . import errors


class BasePostprocessor(object):
    def __init__(self, configuration={}, **kwargs):
        if not hasattr(self, 'configuration'):
            self.configuration = {}
        self.configuration.update(configuration)

        try:
            self._validate_configuration()
        except errors.ImproperlyConfigured as e:
            raise errors.ImproperlyConfigured('Post processor is not properly configured: %s', e)

    def _validate_configuration(self):
        return
