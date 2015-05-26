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
    def parse(self, data, *args):
        try:
            return data['result']['resolvedQuery']
        except (ValueError, KeyError):
            raise UnableToParse


class ActionParser(SimpleParser):
    def _get_result_and_action(self, data):
        try:
            result = data['result']
        except KeyError:
            raise UnableToParse

        return result, result.get('action', '')

    def _to_json(self, result, action):
        return json.dumps({
            'action': action,
            'parameters': result.get('parameters', {}),
            'fulfillment': result.get('fulfillment', '')
        })

    def _simple_parse(self, data):
        return super(ActionParser, self).parse(data)

    def parse(self, data, *args):
        result, action = self._get_result_and_action(data)
        if not action or '.unknown' in action:
            # Could be fulfillment
            fulfillment = result.get('fulfillment', '')
            if fulfillment and fulfillment.get('speech', ''):
                return json.dumps({
                    'action': 'apiai:fulfillment',
                    'fulfillment': fulfillment['speech']
                })

            # Just normal STT
            return self._simple_parse(data)

        return self._to_json(result, action)


class SelectedActionsParser(SimpleParser):
    def parse(self, data, stt, *args):
        result, action = self._get_result_and_action(data)

        if action in stt.selected_actions:
            return self._to_json
            # Could be fulfillment
            fulfillment = result.get('fulfillment', '')
            if fulfillment and fulfillment.get('speech', ''):
                return json.dumps({
                    'action': 'apiai:fulfillment',
                    'fulfillment': fulfillment['speech']
                })

            # Just normal STT
            return self._simple_parse(data)

        return json.dumps({
            'action': action,
            'parameters': result.get('parameters', {}),
            'fulfillment': result.get('fulfillment', '')
        })


PARSERS = {
    'simple': SimpleParser,
    'action': ActionParser,
    'selected_actions': SelectedActionsParser,
}


class ApiaiSpeechToText(minion.sensing.postprocessors.BasePostprocessor):
    def __init__(self, name, configuration={}):
        super(ApiaiSpeechToText, self).__init__(name, configuration)
        self.CLIENT_ACCESS_TOKEN = self.get_configuration('CLIENT_ACCESS_TOKEN')
        self.SUBSCRIBTION_KEY = self.get_configuration('SUBSCRIBTION_KEY')

        # Select the parser according to configuration or default to simple parser
        parser_class = self.get_configuration('parser', 'simple')
        self.parser = PARSERS[parser_class]()
        # Used for selected actions parser
        # TODO Do we really want to set this on the object and not on the parser?
        self.selected_actions = self.get_configuration('selected_actions', [])
        self.ai = apiai.ApiAI(self.CLIENT_ACCESS_TOKEN, self.SUBSCRIBTION_KEY)

    def _validate_configuration(self):
        if not self.get_configuration('CLIENT_ACCESS_TOKEN'):
            raise minion.core.components.exceptions.ImproperlyConfigured('CLIENT_ACCESS_TOKEN is required for Apiai')
        if not self.get_configuration('SUBSCRIBTION_KEY'):
            raise minion.core.components.exceptions.ImproperlyConfigured('SUBSCRIBTION_KEY is required for Apiai')

    def process(self, data):
        request = self.ai.voice_request()
        request.send(data)

        response = request.getresponse()

        try:
            data = json.loads(response.read())
            logger.debug('Data received from API.ai %s', data)
            return self.parser.parse(data, self)
        except (ValueError, UnableToParse):
            # Acceptable errors which just mean we couldn't understand
            raise minion.sensing.exceptions.DataUnaivalable
