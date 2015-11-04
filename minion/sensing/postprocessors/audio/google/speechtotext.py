import minion.postprocessors
import minion.core.utils.functions
import random
import requests
import multiprocessing
import json
import six

logger = multiprocessing.get_logger()


class GoogleSpeechToText(minion.postprocessors.BasePostprocessor):
    url = 'http://www.google.com/speech-api/v2/recognize'

    @minion.core.utils.functions.configuration_getter
    def get_url(self):
        return self.url

    @minion.core.utils.functions.configuration_getter
    def get_type(self):
        return 'flac'

    @minion.core.utils.functions.configuration_getter
    def get_lang(self):
        return 'en-us'

    @minion.core.utils.functions.configuration_getter
    def get_client(self):
        return 'chromium'

    @minion.core.utils.functions.configuration_getter
    def get_content_type(self):
        return 'audio/x-flac; rate=16000;'

    @minion.core.utils.functions.configuration_getter
    def get_keys(self):
        return []

    def get_key(self):
        if isinstance(self.get_keys(), six.string_types):
            return self.get_keys()
        else:
            return random.choice(self.get_keys())

    def _validate_config(self):
        if not self.get_key():
            raise minion.core.components.ImproperlyConfigured('You need to provide at least one Google Speech API key')

    def _build_request_parameters(self, data):
        params = {
            'lang': self.get_lang(),
            'client': self.get_client(),
            'key': self.get_key(),
        }
        headers = {
            'Content-Type': self.get_content_type(),
        }
        files = {
            'file': ('file.{}'.format(self.get_type()), data)
        }

        return {
            'params': params,
            'headers': headers,
            'files': files,
        }

    def _get_google_response(self, parameters):
        return requests.post(self.get_url(), **parameters)

    def process(self, data):
        request_parameters = self._build_request_parameters(data)
        # TODO handle errors
        response = self._get_google_response(request_parameters)

        lines = response.text.split('\n')

        message = 'ERROR Unable to translate speech to text'
        for line in lines:
            try:
                content = json.loads(line)
            except ValueError:
                logger.error('Unable to load json content %s', line)
                continue
            results = content.get('result', [])
            if results.__len__():
                result = results[0]
                message = result['alternative'][0]['transcript']
                break
        logger.debug('Decoded message from Google STT: %s', message)
        return message
