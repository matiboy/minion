import apiai
import json
import minion.sensing.postprocessors
import minion.sensing.exceptions
import minion.core.components.exceptions
import multiprocessing

logger = multiprocessing.get_logger()


class UnableToParse(Exception):
    pass


class SimpleParser(object):
    def parse(self, data):
        try:
            return data['result']['resolvedQuery']
        except (ValueError, KeyError):
            raise UnableToParse


class ActionParser(SimpleParser):
    def parse(self, data):
        try:
            result = data['result']
        except KeyError:
            raise UnableToParse

        action = result.get('action', '')

        if not action:
            # Could be fulfillment
            fulfillment = result.get('fulfillment', '')
            if fulfillment:
                return 'apiai:fulfillment|{}'.format(fulfillment)

            # Just normal STT
            return super(ActionParser, self).parse(data)

        # cant rely on json dumps to keep action first
        return json.dumps({
            'action': action,
            'parameters': result.get('parameters', {}),
            'fulfillment': result.get('fulfillment', '')
        })


PARSERS = {
    'simple': SimpleParser,
    'action': ActionParser
}


class ApiaiSpeechToText(minion.sensing.postprocessors.BasePostprocessor):
    def __init__(self, name, configuration={}):
        super(ApiaiSpeechToText, self).__init__(name, configuration)
        self.CLIENT_ACCESS_TOKEN = self.get_configuration('CLIENT_ACCESS_TOKEN')
        self.SUBSCRIBTION_KEY = self.get_configuration('SUBSCRIBTION_KEY')

        # Select the parser according to configuration or default to simple parser
        parser_class = self.get_configuration('parser', 'simple')
        self.parser = PARSERS[parser_class]()

    def _validate_configuration(self):
        if not self.get_configuration('CLIENT_ACCESS_TOKEN'):
            raise minion.core.components.exceptions.ImproperlyConfigured('CLIENT_ACCESS_TOKEN is required for Apiai')
        if not self.get_configuration('SUBSCRIBTION_KEY'):
            raise minion.core.components.exceptions.ImproperlyConfigured('SUBSCRIBTION_KEY is required for Apiai')

    def process(self, data):
        ai = apiai.ApiAI(self.CLIENT_ACCESS_TOKEN, self.SUBSCRIBTION_KEY)
        request = ai.voice_request()
        request.send(data)

        response = request.getresponse()

        try:
            data = json.loads(response.read())
            logger.debug(data)
            return self.parser.parse(data)
        except (ValueError, UnableToParse):
            # Acceptable errors which just mean we couldn't understand
            raise minion.sensing.exceptions.DataUnaivalable
