import minion.understanding.api
import multiprocessing
import string

logger = multiprocessing.get_logger()

URL = 'http://www.iheartquotes.com/api/v1/random?format=json'


class RandomQuote(minion.understanding.api.JsonAPICommand):
    configuration = {
        'url': URL,
        'method': 'get',
        'json_path': '$.quote',
        'expressions': ['quote'],
        'action': 'minion:speak'
    }

    def _post_process(self, results):
        acceptable = string.ascii_letters + ' ,!.-'

        for result in results:
            # clear everything except letters and spaces
            result = ''.join([x.lower() for x in result if x in acceptable]).replace('.', '. ').replace('--', '  ')

            # Let's only use one result
            return (result,)
