import json
import minion.utils.module_loading
import os
import multiprocessing
import logging
import time

settings = os.getenv('MINION_SETTINGS', 'settings.json')

if __name__ == '__main__':
    multiprocessing.log_to_stderr(logging.DEBUG)
    try:
        with open(settings) as settings_file:
            brain_settings = json.load(settings_file)
    except IOError:
        raise IOError('Settings file not found: {}. Set the environment variable MINION_SETTINGS to the correct path'.format(settings))

    # Ativate the communication system
    try:
        nerve_settings = brain_settings['nerve']
    except KeyError:
        raise KeyError('You must provide a nervous system')
    nervous_system_class = minion.utils.module_loading.import_string(nerve_settings['class'])
    nervous_system = nervous_system_class(**nerve_settings)

    # Register all commands
    logger = multiprocessing.get_logger()
    command_instances = []
    for command in brain_settings.get('commands', []):
        command_class = minion.utils.module_loading.import_string(command['class'])
        # instantiate
        command_instance = command_class(configuration=command.get('configuration', {}), name=command.get('name'))
        command_instances.append(command_instance)

    while True:
        for m in nervous_system.listen():
            logger.debug('Command received: %s', m)
            if m['type'] == 'message':
                command = m['data']

                for c in command_instances:
                    command_matches = c.matches(command)
                    if command_matches:
                        action, message = c.understand(*command_matches.groups())
                        nervous_system.publish(channel=action, message=message)

        time.sleep(brain_settings.get('delay', 0.01))
