import inquirer
import minion.core.components

defines = {
    minion.core.components.Types.ACTUATOR: [
        {
            'name': 'Commit to redis memory',
            'class': 'minion.acting.memory.redis.CommitToMemory',
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
            ]
        }
    ]
}
