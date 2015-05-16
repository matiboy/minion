import inquirer
import minion.core.components

defines = {
    minion.core.components.Types.ACTUATOR: [
        {
            'name': 'MacOsx say command',
            'class': 'minion.acting.mouth.macosx.say.SimpleSay',
            'default_channel': 'minion:speak',
            'description': '''
# MacOsx say command
# Availability: Mac OS X only
#
# Uses the built-in "say" command in MacOsx to say stuff
#
# Refer to https://developer.apple.com/library/mac/documentation/Darwin/Reference/ManPages/man1/say.1.html
#
# Only the voice selection (-v) option is implemented
#
            ''',
            'questions': [
                inquirer.List('voice', message='Select a voice', choices=[
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
                ]),
            ]
        }
    ]
}
