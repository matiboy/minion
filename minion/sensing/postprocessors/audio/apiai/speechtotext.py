import apiai
import json
import tempfile
import minion.sensing.postprocessors
import minion.sensing.exceptions
import minion.core.components.exceptions
import multiprocessing

logger = multiprocessing.get_logger()


class ApiaiSpeechToText(minion.sensing.postprocessors.BasePostprocessor):
    configuration = {
        'delete_audio_file': True # Set this to false to debug by keeping audio file after request
    }

    def __init__(self, name, configuration={}):
        super(ApiaiSpeechToText, self).__init__(name, configuration)
        self.CLIENT_ACCESS_TOKEN = self.get_configuration('CLIENT_ACCESS_TOKEN')
        self.SUBSCRIBTION_KEY = self.get_configuration('SUBSCRIBTION_KEY')

    def _validate_configuration(self):
        if not self.get_configuration('CLIENT_ACCESS_TOKEN'):
            raise minion.core.components.exceptions.ImproperlyConfigured('CLIENT_ACCESS_TOKEN is required for Apiai')
        if not self.get_configuration('SUBSCRIBTION_KEY'):
            raise minion.core.components.exceptions.ImproperlyConfigured('SUBSCRIBTION_KEY is required for Apiai')

    def process(self, data):
        ai = apiai.ApiAI(self.CLIENT_ACCESS_TOKEN, self.SUBSCRIBTION_KEY)
        request = ai.voice_request()
        with tempfile.NamedTemporaryFile(delete=self.get_configuration('delete_audio_file')) as f:
            f.write(data)
            bytessize = 2048
            data = f.read(bytessize)
            logger.debug('Writing to temporary file %s', f.name)
            if not self.get_configuration('delete_audio_file'):
                logger.debug('File will be kept after post-process')
            while data:
                request.send(data)
                data = f.read(bytessize)

        response = request.getresponse()

        try:
            data = json.loads(response.read())
            return data['result']['resolvedQuery']
        except (ValueError, KeyError,):
            # Acceptable errors which just mean we couldn't understand
            # TODO or should we raise?
            raise minion.sensing.exceptions.DataUnaivalable
