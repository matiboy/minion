import minion.core.components.exceptions
import minion.core.utils.functions
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

    @minion.core.utils.functions.configuration_getter
    def get_value(self):
        # Default to 1 for cases where just setting a value is sufficient
        return 1

    @minion.core.utils.functions.configuration_getter
    def get_state(self):
        return None

    def _build_command(self, original_command, *commands):
        return 'set {} {}'.format(self.get_state(), self.get_value())

    def _understand(self, original_command, *commands):
        body = self._build_command(original_command, *commands)
        return minion.understanding.operations.UnderstandingOperation(self.get_command(), body)


class ForgetState(StateToMemory):
    def _build_command(self, original_command, *commands):
        return 'forget {}'.format(self.get_state())
