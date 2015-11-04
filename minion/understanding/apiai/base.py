import json
import minion.understanding.base
import minion.understanding.exceptions
import multiprocessing

logger = multiprocessing.get_logger()


class ApiaiBaseCommand(minion.understanding.base.BaseCommand):
    configuration = {
        'host': 'localhost',
        'db': 0,
        'port': '',
        'acknowledge': True
    }

    def __init__(self, name, configuration):
        super(ApiaiBaseCommand, self).__init__(name, configuration)

        self.actions = self.get_configuration('actions')

    def matches(self, command):
        # Try to find an action
        try:
            command = json.loads(command)
            action = command['action']
        except (ValueError, KeyError, TypeError) as e:
            # TypeError could be from command being json loadable but being a dict
            # The rest would be from Json parsing
            logger.debug(e)
            raise minion.understanding.exceptions.DoesNotMatch

        # Check if this command understands said action
        if action in self.actions:
            return [action, command.get('parameters', {}), command.get('fulfillment', '')]

        raise minion.understanding.exceptions.DoesNotMatch
