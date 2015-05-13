import json
import minion.core.utils.module_loading
import minion.understanding.errors
import minion.core
import minion.core.components.exceptions
import os
import multiprocessing
import logging


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

    # Start all the actuators
    commands_details = settings.get('commands', [])

    # Might raise NameConflict if two commands have the same name
    my_minion.attach_commands(*commands_details)

    my_minion.loop()
