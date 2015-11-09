import minion.core.components

defines = {
    minion.core.components.Types.ACTUATOR: [
        {
            'name': 'Pyttsx TTS',
            'class': 'minion.acting.mouth.pyttsx.pyttsx.SimpleSay',
            'default_channel': 'minion:speak',
            'description': '''
<h3>Pyttsx based Text To Speech</h3>
<p>Refer to <a href="https://pyttsx.readthedocs.org/en/latest/engine.html">https://pyttsx.readthedocs.org/en/latest/engine.html</a></p>
<p>On Raspberry Pi/Banana Pi etc, make sure Jack service is running by using the shell command jack_control start</p>
            ''',
            'setup': [
                {
                    'name': 'voice',
                    'default': '',
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
