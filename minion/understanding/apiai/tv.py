from . import base
import minion.understanding.operations
import multiprocessing
import minion.core.utils


logger = multiprocessing.get_logger()


class Tv(base.ApiaiBaseCommand):
    threaded = True

    @minion.core.utils.functions.configuration_getter
    def _get_acknowledge(self):
        return False

    def _understand(self, original_command, action, parameters, fulfillment):
        logger.debug('ORIGINAL_COMMAND {}'.format(original_command))
        operations = [
            minion.understanding.operations.UnderstandingOperation(self.get_configuration('lirc_channel', 'minion:lirc'), 'tv KEY_POWER'),
        ]
        if self._get_acknowledge() and fulfillment and fulfillment.get('speech', ''):
            ack = fulfillment['speech']
            operations.append(minion.understanding.operations.UnderstandingOperation('minion:speak', '{prefix} {ack}'.format(prefix=self.get_configuration('fulfillment_prefix', ''), ack=ack)),)
        return operations
