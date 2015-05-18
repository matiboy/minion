import minion.postprocessors
import random
import requests
import multiprocessing
import json

logger = multiprocessing.get_logger()


class GoogleSpeechToText(minion.postprocessors.BasePostprocessor):
    configuration = {
        'url': 'http://www.google.com/speech-api/v2/recognize',
        'lang': 'en-us',
        'client': 'chromium',
        'Content-Type': 'audio/x-flac; rate=16000;',
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

        # TODO handle errors
        response = requests.post(self.configuration['url'], params=params, headers=headers, files=files)

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
        logger.debug(message)
        return message