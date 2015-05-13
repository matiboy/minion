import minion.understanding.base
import minion.understanding.repeat


class Decide(minion.understanding.repeat.AlwaysSaySomethingRandom):
    configuration = {
        'action': 'minion:speak',
        'expressions': ['random (?P<decision>.+)'],
        'split': ' '
    }

    def get_choices(self, original_command, *commands):
        command = commands[0]
        return command.split(self.get_configuration('split'))
