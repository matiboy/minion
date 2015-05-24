import minion.core.components.exceptions
import minion.understanding.base
import minion.understanding.operations


class StateToMemory(minion.understanding.base.BaseCommand):
    configuration = {
        'action': 'minion:committomemory',
        'expressions': []
    }

    def _validate_configuration(self):
        if 'state' not in self._configuration:
            raise minion.core.components.exceptions.ImproperlyConfigured('State name is required')

    def get_value(self):
        # Default to 1 for cases where just setting a value is sufficient
        return self.get_configuration('value', 1)

    def _understand(self, original_command, *commands):
        return minion.understanding.operations.UnderstandingOperation(self.get_command(), self.get_value())
