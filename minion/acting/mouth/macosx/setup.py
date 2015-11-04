import minion.core.components

defines = {
    minion.core.components.Types.ACTUATOR: [
        {
            'name': 'MacOsx say command',
            'class': 'minion.acting.mouth.macosx.say.SimpleSay',
            'default_channel': 'minion:speak',
            'description': '''
<h3>MacOsx say command</h3>
<h4>Availability: Mac OS X only</h4>
<p>Uses the built-in "say" command in MacOsx to say stuff</p>
<p>Refer to the <a href="https://developer.apple.com/library/mac/documentation/Darwin/Reference/ManPages/man1/say.1.html">say documentation</a>
<p>Only the voice selection (-v) option is implemented</p>
            ''',
            'setup': [
                {
                    'name': 'voice',
                    'default': 'localhost',
                    'type': 'select',
                    'message': 'Select voice',
                    'choices': [
                        'Bruce',
                        'Agnes',
                        'Kathy',
                        'Princess',
                        'Vicki',
                        'Victoria',
                        'Alex',
                        'Fred',
                        'Junior',
                        'Ralph',
                    ]
                }
            ],
            'requirements': ()
        }
    ]
}
