from . import base
import minion.understanding.operations


class Warehouse(base.ApiaiBaseCommand):
    threaded = True

    def _build_key(self, **parameters):
        return 'warehouse:{what}:{where}'.format(**parameters)

    def _understand(self, original_command, action, parameters, fulfillment):
        key = self._build_key(**parameters)
        operations = [
            minion.understanding.operations.UnderstandingOperation(self.get_configuration('memory_channel', 'minion:committomemory'), 'set {key} {value}'.format(key=key, value=parameters['number'])),
        ]
        if self.get_configuration('acknowledge', False) and fulfillment and fulfillment.get('speech', ''):
            ack = fulfillment['speech']
            operations.append(minion.understanding.operations.UnderstandingOperation('minion:speak', '{prefix} {ack}'.format(prefix=self.get_configuration('fulfillment_prefix', ''), ack=ack)),)
        # Send to what we expect is a commit to memory
        return operations
