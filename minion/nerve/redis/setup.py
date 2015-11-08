import minion.core.components

defines = {
    minion.core.components.Types.NERVOUS_SYSTEM: [
        {
            'name': 'Redis',
            'class': 'minion.nerve.redis.redis.NervousSystem',
            'description': '''
<h3>Redis based nervous system.</h3>

<p>Fast event based system.</p>
<p>Set up host, port, db and password according to your environment</p>
            ''',
            'setup': [
                {
                    'name': 'host',
                    'default': 'localhost',
                    'type': 'input',
                    'message': 'Select Redis host'
                },
                {
                    'name': 'port',
                    'default': '6379',
                    'type': 'input',
                    'message': 'Select Redis port'
                },
                {
                    'name': 'db',
                    'default': '0',
                    'type': 'input',
                    'message': 'Select Redis db'
                },
                {
                    'name': 'password',
                    'default': '',
                    'type': 'input',
                    'message': 'Redis password'
                }
            ],
            'requirements': (
                'redis',
            )
        }
    ]
}
