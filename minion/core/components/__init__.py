from . import class_validation
from . import exceptions


class Types():
    ACTUATOR = 'actuators'
    COMMAND = 'commands'
    NERVOUS_SYSTEM = 'nerve'
    PRE_PROCESSOR = 'pre_processors'
    POST_PROCESSOR = 'post_processors'
    SENSOR = 'sensors'


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

    def get_configuration_dict(self, *args):
        return {x: self.get_configuration(x) for x in args}

    def requires_configuration_key(self, key):
        if key not in self._configuration:
            raise exceptions.ImproperlyConfigured('Key <{}> is required'.format(key))

    def requires_non_empty_configuration(self, key):
        if not self.get_configuration(key):
            raise exceptions.ImproperlyConfigured('Configuration for <{}> should not be empty'.format(key))

    def _validate_configuration(self):
        """
            Should raise ImproperlyConfigured if any issue
        """
        pass


class NervousComponent(BaseComponent):
    """
        Very similar to BaseComponent but requires a nervous system instance to be passed
    """
    def __init__(self, name, nervous_system, configuration={}):
        if not class_validation.is_nervous_system(nervous_system):
            raise exceptions.ImproperlyConfigured('Nervous system does not appear to have the necessary methods')
        self.nervous_system = nervous_system
        super(NervousComponent, self).__init__(name, configuration)
