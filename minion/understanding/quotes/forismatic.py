import minion.understanding.api

URL = 'http://api.forismatic.com/api/1.0/'


class RandomQuote(minion.understanding.api.JsonAPICommand):
    configuration = {
        'method': 'post',
        'lang': 'en',
        'json_path': '$',
        'url': URL,
        'action': 'minion:speak',
        'expressions': ['quote']
    }

    def _build_API_call(self, original_command, *commands):
        url, nothing = super(RandomQuote, self)._build_API_call(original_command, commands)
        kwargs = {
            'data': {
                'method': 'getQuote',
                'lang': self.get_configuration('lang'),
                'format': 'json'
            }
        }

        return url, kwargs

    def _post_process(self, results):
        return ('{quoteText} by {quoteAuthor}'.format(**result) for result in results)
