from __future__ import absolute_import
import minion.acting.base
import minion.core.utils.functions
import minion.core.utils.console
import multiprocessing
import requests
import json

logger = multiprocessing.get_logger()


class Mopidy(minion.acting.base.BaseActuator):
    """
    Mopidy actuator using requests
    """
    url_pattern = 'http://{host}:{port}/mopidy/rpc'

    def __init__(self, name, configuration, channels=[], **kwargs):
        super(Mopidy, self).__init__(name, configuration, channels, **kwargs)

    def _validate_configuration(self):
        self.url = self.url_pattern.format(host=self._get_host(), port=self._get_port())
        # Let's at least check that we get a 200 from a simple POST
        r = requests.post(self.url)
        if not r.ok:
            raise minion.core.components.exceptions.ImproperlyConfigured('Did not get a response from the Mopidy server')

    @minion.core.utils.functions.configuration_getter
    def _get_host(self):
        return 'localhost'

    @minion.core.utils.functions.configuration_getter
    def _get_port(self):
        return 6680

    def _parse_command(self, command):
        # Split at first white space
        method, _, rest = command.partition(' ')
        return getattr(self, method), rest

    def act(self, *args, **kwargs):
        command = args[0]
        try:
            method, rest = self._parse_command(command)
        except AttributeError:
            minion.core.utils.console.console_error('Mopidy command <{}> does not exist '.format(command))

        method(rest)

    def _process_request(self, method, params=None):
        data = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method
        }

        if params is not None:
            data['params'] = params

        return requests.post(self.url, data=json.dumps(data))

    def next_song(self, rest):
        # Rest is not needed here
        self._process_request('core.playback.next')

    def previous_song(self, rest):
        # Rest is not needed here
        self._process_request('core.playback.previous')

    def play(self, rest):
        # Rest is not needed here
        self._process_request('core.playback.play')

    def stop(self, rest):
        # Rest is not needed here
        self._process_request('core.playback.stop')

    def shuffle_on(self, rest):
        self._process_request('core.tracklist.set_random', [True])

    def shuffle_off(self, rest):
        self._process_request('core.tracklist.set_random', [False])

    def repeat_on(self, rest):
        self._process_request('core.tracklist.set_repeat', [True])

    def repeat_off(self, rest):
        self._process_request('core.tracklist.set_repeat', [False])

    def _get_volume(self):
        try:
            return self._process_request('core.mixer.get_volume').json()['result']
        except:
            # How to handle errors?
            return 50

    def _set_volume(self, calculate_volume):
        # Get volume
        volume = self._get_volume()
        volume = calculate_volume(volume)

        # Rest is not needed here
        self._process_request('core.mixer.set_volume', [volume])

    def volume_up(self, rest):
        def calculate_volume(v):
            return min(v+10, 100)

        self._set_volume(calculate_volume)

    def volume_down(self, rest):
        def calculate_volume(v):
            return max(v-10, 0)

        self._set_volume(calculate_volume)
