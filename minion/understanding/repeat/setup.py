import minion.core.components


defines = {
    minion.core.components.Types.COMMAND: [
        {
            'name': 'Always say something',
            'class': 'minion.understanding.repeat.AlwaysSaySomething',
            'description': '''
<h3>Always say something</h3>
<h4>Description</h4>
<p>As soon as command matches expressions, a string will be output to the action channel. The string never changes</p>
            ''',
            'setup': [
            {
                'name': 'what',
                'default': 'Hi',
                'type': 'input',
                'message': 'Outputted string'
            }
            ,],
            'requirements': [],
        }
    ]
}
