import minion.core.components

defines = {
    minion.core.components.Types.COMMAND: [
        {
            'name': 'Redis',
            'class': 'minion.understanding.calendar.ics.ics.IcsCalendarTodayEvents',
            'description': '''
# ICS reader and parser for today's events
#
# Can read from local ICS file or from URL
#
# Grabs today's events and broadcasts a single speech command to read them out
            ''',
            'setup': [
                {
                    'name': 'resource',
                    'default': '',
                    'type': 'input',
                    'message': 'Resource url or path'
                }
            ],
            'requirements': (
                'ics',
                'arrow',
            )
        },
        {
            'name': 'Redis',
            'class': 'minion.understanding.calendar.ics.ics.IcsCalendarTomorrowEvents',
            'description': '''
# ICS reader and parser for tomorrow's events
#
# Can read from local ICS file or from URL
#
# Grabs tomorrow's events and broadcasts a single speech command to read them out
            ''',
            'setup': [
                {
                    'name': 'resource',
                    'default': '',
                    'type': 'input',
                    'message': 'Resource url or path'
                }
            ],
            'requirements': (
                'ics',
                'arrow',
            )
        }
    ]
}
