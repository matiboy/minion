import minion.understanding.base


class RepeatAfterMe(minion.understanding.base.BaseCommand):
    configuration ={
        'action': 'minion:speak',
        'expressions': [r'^repeat after me (?P<what_to_repeat>.*)$']
    }

    def understand(self, *commands):
        # Doesn't expect multi
        command = commands[0]
        return self.configuration['action'], command
