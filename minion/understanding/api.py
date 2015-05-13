from . import base
from . import operations
import jsonpath_rw
import minion.core.components.exceptions
import multiprocessing
import requests

logger = multiprocessing.get_logger()


# Parsers
class JsonParser(object):
    def __init__(self, json_path):
        self.json_path = jsonpath_rw.parse(json_path)

    def get_data(self, response):
        logger.debug(response)
        return response.json()

    def parse(self, response):
        # Get data from response
        try:
            data = self.get_data(response)
        except ValueError:
            logger.error('Unable to parse data from request')
            return None

        # Now parse
        return [x.value for x in self.json_path.find(data)]


# TODO!!
class XMLParser(object):
    pass


class APICommand(base.BaseCommand):
    configuration = {
        'method': 'get'
    }
    threaded = True

    def _validate_configuration(self):
        if not self.get_configuration('url'):
            raise minion.core.components.exceptions.ImproperlyConfigured('URL is required for API command')

    def _build_API_call(self, original_command, *commands):
        return (self.get_configuration('url'), {})

    def _understand(self, original_command, *commands):
        api_call, kwargs = self._build_API_call(original_command, *commands)
        method = getattr(requests, self.get_configuration('method', 'get'))
        response = method(api_call, **kwargs)
        results = self.parser.parse(response)

        # Post process results if need be
        results = self._post_process(results)

        return (operations.UnderstandingOperation(self.get_command(), command) for command in results)

    def _post_process(self, results):
        return results

class JsonAPICommand(APICommand):
    def __init__(self, name, configuration):
        super(JsonAPICommand, self).__init__(name, configuration)
        self.parser = JsonParser(self.get_configuration('json_path', ''))

    def _validate_configuration(self):
        super(JsonAPICommand, self)._validate_configuration()
        if not self.get_configuration('json_path'):
            raise minion.core.components.exceptions.ImproperlyConfigured('URL is required for API command')
