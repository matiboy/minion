import minion.understanding.base
import random


class RepeatAfterMe(minion.understanding.base.BaseCommand):
    configuration = {
        'action': 'minion:speak',
        'expressions': [r'^repeat after me (?P<what_to_repeat>.*)$']
    }

    def _understand(self, original_command, *commands):
        # Doesn't expect multi
        command = commands[0]
        return minion.understanding.base.UnderstandingCommand(self.get_command(), command)


class AlwaysSaySomething(minion.understanding.base.BaseCommand):
    configuration = {
        'action': 'minion:speak',
        'expressions': [r'^i think (?P<what_i_think>.*)$'],
        'what': 'i think you are right'
    }

    def _what_to_say(self, original_command, *commands):
        return self.get_configuration('what')

    def _understand(self, original_command, *commands):
        what_to_say = self._what_to_say(original_command, *commands)
        return minion.understanding.base.UnderstandingCommand(self.get_command(), what_to_say)


class AlwaysSaySomethingRandom(AlwaysSaySomething):
    def _what_to_say(self, original_command, *commands):
        return random.choice(self.get_configuration('choices'))
