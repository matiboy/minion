import minion.core.components


defines = {
    minion.core.components.Types.COMMAND: [
        {
            'name': 'Mopidy play command',
            'class': 'minion.understanding.mopidy.mopidy.NextSong',
            'description': '''
<h3>Modipy play command</h3>
<h4>Description</h4>
<p>Transforms any of the patterns into a next:song command understandable by the Mopidy actuator</p>
            ''',
            'setup': [],
            'requirements': [],
        }
    ]
}
