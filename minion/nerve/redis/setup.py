import minion.core.components

defines = {
    minion.core.components.Types.NERVOUS_SYSTEM: [
        {
            'name': 'Redis',
            'class': 'minion.nerve.redis.redis.NervousSystem',
            'description': '''
# Redis based nervous system.
#
# Fast event based system.
# Set up host, port and db according to your environment
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
                }
            ],
            'requirements': (
                'redis',
            )
        }
    ]
}
