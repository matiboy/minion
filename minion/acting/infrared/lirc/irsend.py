from __future__ import absolute_import
import minion.acting.base
import minion.core.utils.functions
import minion.core.utils.console
import multiprocessing

logger = multiprocessing.get_logger()


class IrsendActuator(minion.acting.base.ShellCommandActuator):
    """
    Infrared actuator using the irsend command to send signals
    This expects an instance of lircd to be running
    """
    @minion.core.utils.functions.configuration_getter
    def _get_remote_control_name(self):
        return 'astro'

    def _build_command(self, *args, **kwargs):
        # Clean up cause it doesnt seem to like quotes
        keys = [x.replace('"', '') for x in list(args)]

        return ['irsend', 'SEND_ONCE', self._get_remote_control_name()] + keys
