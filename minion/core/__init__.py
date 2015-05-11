from .components import exceptions
import minion.utils.module_loading


class Minion(object):
    def __init__(self):
        pass

    def attach_nervous_system(self, configuration):
        if 'name' not in configuration:
            raise exceptions.ImproperlyConfigured('Name is required for nervous system')

        nervous_system_class = minion.utils.module_loading.import_string(configuration['class'])
        self.nervous_system = nervous_system_class(**configuration)
