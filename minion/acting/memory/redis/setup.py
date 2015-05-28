import inquirer
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
            'questions': [
                inquirer.Text('host', message='Redis host', default='localhost'),
                inquirer.Text('port', message='Redis port', default='6379'),
                inquirer.Text('db', message='Redis db', default='0'),
            ],
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
