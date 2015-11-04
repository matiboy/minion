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
            if fulfillment and fulfillment.get('speech', ''):
                return json.dumps({
                    'action': 'apiai:fulfillment',
                    'fulfillment': fulfillment['speech']
                })

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


class ApiaiText(minion.sensing.postprocessors.BasePostprocessor):
    def __init__(self, name, configuration={}):
        super(ApiaiText, self).__init__(name, configuration)
        self.CLIENT_ACCESS_TOKEN = self.get_configuration('CLIENT_ACCESS_TOKEN')
        self.SUBSCRIBTION_KEY = self.get_configuration('SUBSCRIBTION_KEY')

        # Select the parser according to configuration or default to simple parser
        parser_class = self.get_configuration('parser', 'simple')
        self.parser = PARSERS[parser_class]()
        self.ai = apiai.ApiAI(self.CLIENT_ACCESS_TOKEN, self.SUBSCRIBTION_KEY)

    def _validate_configuration(self):
        if not self.get_configuration('CLIENT_ACCESS_TOKEN'):
            raise minion.core.components.exceptions.ImproperlyConfigured('CLIENT_ACCESS_TOKEN is required for Apiai')
        if not self.get_configuration('SUBSCRIBTION_KEY'):
            raise minion.core.components.exceptions.ImproperlyConfigured('SUBSCRIBTION_KEY is required for Apiai')

    def process(self, data):
        request = self.ai.text_request()
        print 'DATADATA', data
        request.query = data

        response = request.getresponse()

        try:
            resp = response.read()
            print resp
            data = json.loads(resp)
            print data
            logger.debug(data)
            return self.parser.parse(data)
        except (ValueError, UnableToParse):
            # Acceptable errors which just mean we couldn't understand
            raise minion.sensing.exceptions.DataUnaivalable
