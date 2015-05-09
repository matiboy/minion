import apiai
import json
import tempfile
import minion.postprocessors
import minion.postprocessors.errors
import multiprocessing

logger = multiprocessing.get_logger()


class ApiaiSpeechToText(minion.postprocessors.BasePostprocessor):
    configuration = {}

    def _validate_configuration(self):
        if not self.configuration.get('CLIENT_ACCESS_TOKEN'):
            raise minion.postprocessors.errors.ImproperlyConfigured('CLIENT_ACCESS_TOKEN is required for Apiai')
        if not self.configuration.get('SUBSCRIBTION_KEY'):
            raise minion.postprocessors.errors.ImproperlyConfigured('SUBSCRIBTION_KEY is required for Apiai')

    def process(self, data):
        CLIENT_ACCESS_TOKEN = self.configuration.get('CLIENT_ACCESS_TOKEN')
        SUBSCRIBTION_KEY = self.configuration.get('SUBSCRIBTION_KEY')
        ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN, SUBSCRIBTION_KEY)
        request = ai.voice_request()
        request.send(data)
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(data)
            bytessize = 2048
            data = f.read(bytessize)
            logger.debug(f.name)
            while data:
                request.send(data)
                data = f.read(bytessize)

        response = request.getresponse()

        try:
            data = json.loads(response.read())
            return data['result']['resolvedQuery']
        except ValueError, KeyError:
            # Acceptable errors which just mean we couldn't understand
            # TODO or should we raise?
            pass
