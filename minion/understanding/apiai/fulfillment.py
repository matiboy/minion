from . import base
import minion.understanding.operations


class Fulfillment(base.ApiaiBaseCommand):
    def _understand(self, original_command, action, parameters, fulfillment):
        return minion.understanding.operations.UnderstandingOperation('minion:speak', '{prefix} {ack}'.format(prefix=self.get_configuration('fulfillment_prefix', ''), ack=fulfillment))
