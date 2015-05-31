import minion.core.components


defines = {
    minion.core.components.Types.SENSOR: [
        {
            'name': 'HTTPS API, simply listens on a give port and passes whatever received to its postprocessors',
            'class': 'minion.sensing.https.flask.server.HttpsServer',
            'setup': [],
            'description': '''
# Runs a Flask HTTPS enabled server with a single API point
# Expects POST data to be passed.
# For security purposes, it is better to use the Signature postprocessor
            ''',
            'setup': [
                {
                    'name': 'ip',
                    'default': '0.0.0.0',
                    'type': 'input',
                    'message': 'Server IP'
                },
                {
                    'name': 'port',
                    'default': '20202',
                    'type': 'input',
                    'message': 'Port'
                },
                {
                    'name': 'ssl_certificate',
                    'default': 'server.crt',
                    'type': 'input',
                    'message': 'Path to SSL Certificate'
                },
                {
                    'name': 'ssl_key',
                    'default': 'server.key',
                    'type': 'input',
                    'message': 'Path to SSL Key'
                },
                {
                    'name': 'route',
                    'default': '/banana',
                    'type': 'input',
                    'message': 'Route to listen on'
                }
            ],
            'requirements': (
                'flask',
            )
        }
    ]
}
