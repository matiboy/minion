import minion.core.utils.console
import minion.core.utils.functions
import minion.sensing.exceptions as exceptions
import minion.sensing.base
import multiprocessing
import socket

logger = multiprocessing.get_logger()

class SocketListener(minion.sensing.base.ContinuousSensor):
    period = 0.01

    def __init__(self, name, nervous_system, configuration={}, preprocessors=[], postprocessors=[], **kwargs):
        super(SocketListener, self).__init__(name, nervous_system, configuration, preprocessors, postprocessors, **kwargs)
        try:
            self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        except socket.error as e:
            raise exceptions.ImproperlyConfigured(e)

    @minion.core.utils.functions.configuration_getter
    def _get_path(self):
        return ''

    @minion.core.utils.functions.configuration_getter
    def _get_buffer_size(self):
        return 50

    def _validate_configuration(self):
        self.requires_configuration_key('path')
        self.requires_non_empty_configuration('path')

    def sense(self):
        self.app.run(host=self._get_host(), port=self._get_port(), debug=self._get_debug())
        return self.socket.recv(int(self._get_buffer_size()))

