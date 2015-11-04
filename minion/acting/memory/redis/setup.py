import minion.core.components

defines = {
    minion.core.components.Types.ACTUATOR: [
        {
            'name': 'Commit to redis memory',
            'class': 'minion.acting.memory.redis.commit.CommitToMemory',
            'default_channel': 'minion:committomemory',
            'description': '''
# Commit to redis memory
#
# Changes a value kept is a redis key-value store
#
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
