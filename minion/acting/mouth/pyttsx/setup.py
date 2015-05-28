import minion.core.components

defines = {
    minion.core.components.Types.ACTUATOR: [
        {
            'name': 'Pyttsx TTS',
            'class': 'minion.acting.mouth.pyttsx.pyttsx.SimpleSay',
            'default_channel': 'minion:speak',
            'description': '''
# Pyttsx based Text To Speech
#
# Refer to https://pyttsx.readthedocs.org/en/latest/engine.html
#
# On Raspberry Pi/Banana Pi etc, make sure Jack service is running by using the shell command jack_control start
            ''',
            'setup': [
                {
                    'name': 'voice',
                    'default': 'localhost',
                    'type': 'input',
                    'message': 'Provide voice id (leave empty for default)'
                },
                {
                    'name': 'rate',
                    'default': '150',
                    'type': 'input',
                    'message': 'Speech rate'
                }
            ],
            'requirements': (
                'pyttsx',
            )
        }
    ]
}
