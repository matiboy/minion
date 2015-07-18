import minion.core.components

defines = {
    minion.core.components.Types.ACTUATOR: [
        {
            'name': 'Irsend commands',
            'class': 'minion.acting.infrared.lirc.irsend.Command',
            'default_channel': 'minion:irsend',
            'description': '''
<h3>Irsend wrapper</h3>
            ''',
            'setup': [
                {
                    'name': 'remote_control_name',
                    'default': 'astro',
                    'type': 'input',
                    'message': 'Remote control name'
                }
            ],
            'requirements': ()
        }
    ]
}
