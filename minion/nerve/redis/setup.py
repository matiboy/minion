import inquirer
import minion.core.components

defines = {
    minion.core.components.Types.NERVOUS_SYSTEM: [
        {
            'name': 'Redis',
            'class': 'minion.nerve.redis.redis.NervousSystem',
            'questions': [
                inquirer.Text('host', message='Select Redis host', default='localhost'),
                inquirer.Text('port', message='Select Redis port', default='6379')
            ],
            'requirements': (
                'redis',
            )
        }
    ]
}
