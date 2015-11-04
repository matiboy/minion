import minion.core.components

defines = {
    minion.core.components.Types.ACTUATOR: [
        {
            'name': 'Interface to the Mopidy JSON API',
            'class': 'minion.acting.spotify.mopidy.Mopidy',
            'default_channel': 'minion:mopidy',
            'description': '''
<h3>Mopidy JSON API interface
<h4>Description</h4>
<p>Accepts very specific commands on the nervous system and transforms them into HTTP requests to be processed by a running Mopidy instance</p>
<p>Expects a Mopidy instance to be fully set up including the HTTP plugin</p>
            ''',
            'setup': [
                {
                    'name': 'host',
                    'default': 'localhost',
                    'type': 'input',
                    'message': 'Mopidy host'
                },
                {
                    'name': 'port',
                    'default': 6680,
                    'type': 'input',
                    'message': 'Mopidy port'
                }
            ],
            'requirements': ('requests',)
        }
    ]
}
