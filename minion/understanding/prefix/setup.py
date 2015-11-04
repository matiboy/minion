import minion.core.components


defines = {
    minion.core.components.Types.COMMAND: [
        {
            'name': 'Prefix removal command',
            'class': 'minion.understanding.prefix.prefix.PrefixRemover',
            'description': '''
<h3>Prefix removal command</h3>
<h4>Description</h4>
<p>Will catch all commands that start with given prefix, remove that prefix and broadcast the same command again</p>
<p>If no expressions are provided in the configuration, will user "^<prefix> *" as expression</p>
<p>If no output channel is provided, broadcasts back to same channel</p>
            ''',
            'setup': [
              {
                'type': 'input',
                'name': 'prefix',
                'default': '',
                'message': 'Prefix'
              }
            ],
            'requirements': [],
        }
    ]
}
