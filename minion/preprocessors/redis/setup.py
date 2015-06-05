import minion.core.components

defines = {
    minion.core.components.Types.PRE_PROCESSOR: [
        {
            'name': 'Intents preprocessor - Intent exists',
            'class': 'minion.preprocessors.redis.intents.IntentExists',
            'description': '''
<h3>Intent preprocessor - Intent exists</h3>
<h4>Description</h4>
<p>Checks in Redis that a given intent value exists, otherwise stops pre-processors</p>
<p>You may make this non blocking by setting <i>blocking</i> to false in the config (not available in Big Boss)</p>
            ''',
            'setup': [
                {
                    'name': 'host',
                    'default': 'localhost',
                    'type': 'input',
                    'message': 'Redis host'
                },
                {
                    'name': 'port',
                    'default': 6379,
                    'type': 'input',
                    'message': 'Redis port'
                },
                {
                    'name': 'db',
                    'default': 0,
                    'type': 'input',
                    'message': 'Redis db'
                },
                {
                    'name': 'key',
                    'default': '',
                    'type': 'input',
                    'message': 'Intent key (required)'
                }
            ],
            'requirements': ('redis',)
        }
    ]
}
