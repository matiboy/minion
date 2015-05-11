import json
import minion.utils.module_loading
import minion.understanding.errors
import minion.core
import minion.core.components.exceptions
import os
import multiprocessing
import logging
import time
import threading
import sys


if __name__ == '__main__':
    settings = os.getenv('MINION_SETTINGS', 'settings.json')
    # TODO read that from arguments
    multiprocessing.log_to_stderr(logging.DEBUG)
    try:
        with open(settings) as settings_file:
            settings = json.load(settings_file)
    except IOError:
        raise IOError('Settings file not found: {}. Set the environment variable MINION_SETTINGS to the correct path'.format(settings))

    # Rise, minion
    my_minion = minion.core.Minion()

    # Ativate the communication system
    try:
        nerve_settings = settings['nerve']
    except KeyError:
        raise KeyError('You must provide a nervous system')

    my_minion.attach_nervous_system(nerve_settings)

    # Start all the sensors
    sensor_details = settings.get('sensors', [])

    # Might raise NameConflict if two sensors have the same name
    my_minion.attach_sensors(*sensor_details)

    # Start all the actuators
    actuators_details = settings.get('actuators', [])

    # Might raise NameConflict if two actuators have the same name
    my_minion.attach_actuators(*actuators_details)

    my_minion.loop()
    """logger = multiprocessing.get_logger()
    
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
    """
