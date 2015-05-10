import json
import minion.utils.module_loading
import minion.understanding.errors
import os
import multiprocessing
import logging
import time
import threading

settings = os.getenv('MINION_SETTINGS', 'settings.json')

if __name__ == '__main__':
    multiprocessing.log_to_stderr(logging.DEBUG)
    try:
        with open(settings) as settings_file:
            settings = json.load(settings_file)
    except IOError:
        raise IOError('Settings file not found: {}. Set the environment variable MINION_SETTINGS to the correct path'.format(settings))

    # Ativate the communication system
    try:
        nerve_settings = settings['nerve']
    except KeyError:
        raise KeyError('You must provide a nervous system')
    nervous_system_class = minion.utils.module_loading.import_string(nerve_settings['class'])
    nervous_system = nervous_system_class(**nerve_settings)

    # Start all the sensors
    logger = multiprocessing.get_logger()
    for sensor_details in settings.get('sensors', []):
        sensor_class = minion.utils.module_loading.import_string(sensor_details['class'])

        # instantiate
        sensor = sensor_class(nervous_system, **sensor_details)

        d = multiprocessing.Process(name=sensor_details['configuration'].get('name', 'thread'), target=sensor.run)

        d.start()

    # Register all actuators
    actuator_instances = []
    for actuator_details in settings.get('actuators', []):
        actuator_class = minion.utils.module_loading.import_string(actuator_details['class'])

        # instantiate
        actuator = actuator_class(**actuator_details)
        actuator_instances.append(actuator)

    # Register all commands
    command_instances = []
    for command in settings.get('commands', []):
        command_class = minion.utils.module_loading.import_string(command['class'])
        # instantiate
        try:
            command_instance = command_class(configuration=command.get('configuration', {}), name=command.get('name'))
        except minion.understanding.errors.ImproperlyConfigured as e:
            logger.error('Not adding command: %s', e)
        else:
            command_instances.append(command_instance)

    while True:
        for m in nervous_system.listen():
            logger.debug('Command received: %s', m)
            command = m.get_message()

            # TODO Differentiate between command/action channels
            if m.get_channel() == 'minion:command':
                for c in command_instances:
                    command_matches = c.matches(command)
                    if command_matches:
                        logger.debug('Command <%s> can handle command %s', c, command)
                        c.understand(nervous_system, command, *command_matches.groups())

            else:
                for actuator in actuator_instances:
                    if actuator.can_handle(m.get_channel()):
                        actuator.act(m.get_message())      

        time.sleep(settings.get('delay', 0.01))
