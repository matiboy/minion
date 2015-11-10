import minion.core.components

defines = {
    minion.core.components.Types.SENSOR: [
        {
            'name': 'Unix Socket Listener',
            'class': 'minion.sensing.eyes.filesystem.unix.SocketListener',
            'description': '''
<h3>Unix Socket Listener</h3>
<h4>Description</h4>
<p>This sensor listens to a Unix socket for input</p>
            ''',
            'setup': [
                {
                    'name': 'path',
                    'default': '',
                    'type': 'input',
                    'message': 'Unix Socket Path'
                },
                {
                    'name': 'period',
                    'default': 0.01,
                    'type': 'input',
                    'message': 'Sensing period'
                },
                {
                    'name': 'Buffer size',
                    'default': 50,
                    'type': 'input',
                    'message': 'Maximum buffer size to read from socket'
                }
            ],
            'requirements': ()
        }
    ]
}
