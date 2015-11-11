import minion.understanding.base
import minion.core.utils.functions
import minion.understanding.operations
import random


class RepeatAfterMe(minion.understanding.base.BaseCommand):
    configuration = {
        'action': 'minion:speak',
        'expressions': ['^repeat after me (?P<what_to_repeat>.*)$']
    }

    def _understand(self, original_command, *commands):
        # Doesn't expect multi
        command = commands[0]
        return minion.understanding.operations.UnderstandingOperation(self.get_command(), command)


class AlwaysSaySomething(minion.understanding.base.BaseCommand):
    @minion.core.utils.functions.configuration_getter
    def get_action(self):
        return 'minion:speak'

    @minion.core.utils.functions.configuration_getter
    def get_expressions(self):
        return ['^i think (?P<what_i_think>.*)$']

    @minion.core.utils.functions.configuration_getter
    def get_what(self):
        return 'i think you are right'

    def _understand(self, original_command, *commands):
        what_to_say = self.get_what()
        return minion.understanding.operations.UnderstandingOperation(self.get_action(), what_to_say)


class AlwaysSaySomethingRandom(AlwaysSaySomething):
    def get_choices(self, original_command, *commands):
        return self.get_configuration('choices')

    def _what_to_say(self, original_command, *commands):
        return random.choice(self.get_choices(original_command, *commands))
