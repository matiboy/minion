import json
import minion.understanding.base


class ApiaiBaseCommand(minion.understanding.base.BaseCommand):
    configuration = {
        'host': 'localhost',
        'db': 0,
        'port': ''
    }

    def __init__(self, name, configuration):
        super(ApiaiBaseCommand, self).__init__(name, configuration)

        self.actions = self.get_configuration('actions')

    def matches(self, command):
        # Try to find an action
        try:
            command = json.loads(command)
            action = command['action']
        except (ValueError, KeyError):
            return False

        # Check if this command understands said action
        return action in self.actions
