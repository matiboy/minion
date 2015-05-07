import minion.postprocessors
import random
import requests
import multiprocessing

logger = multiprocessing.get_logger()


class GoogleSpeechToText(minion.postprocessors.BasePostprocessor):
    configuration = {
        'url': 'http://www.google.com/speech-api/v2/recognize',
        'lang': 'en-us',
        'client': 'chromium',
        'Content-Type': 'audio/x-flac; rate 16000;',
        'keys': [],
        'type': 'flac'
    }

    def process(self, data):
        params = {
            'lang': self.configuration['lang'],
            'client': self.configuration['client'],
            'key': random.choice(self.configuration['API_KEY']),
        }
        headers = {
            'Content-Type': self.configuration['Content-Type'],
        }
        files = {
            'file': ('file.{}'.format(self.configuration['type']), data)
        }
        logger.debug(headers)
        logger.debug(params)
        response = requests.post(self.configuration['url'], params=params, headers=headers, files=files)

        lines = response.text.split('\n')

        print lines
        logger.debug(lines)
