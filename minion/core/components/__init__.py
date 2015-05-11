class BaseComponent(object):
    configuration = {}

    def __init__(self, name, configuration={}):
        self.name = name
        self._update_configuration(configuration)
        # Validate config, needs to raise ImproperlyConfigured if any problem
        self._validate_configuration()

    def _update_configuration(self, configuration):
        """
            Copies configuration from class and updates it with passed configuration
            Not recursive
        """
        self._configuration = self.configuration.copy()
        self._configuration.update(configuration)

    def get_configuration(self, key, default=None):
        return self._configuration.get(key, default)

    def _validate_configuration(self):
        """
            Should raise ImproperlyConfigured if any issue
        """
        pass
