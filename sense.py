import json
import minion.utils.module_loading
import os
import multiprocessing
import logging

settings = os.getenv('MINION_SETTINGS', 'settings.json')

if __name__ == '__main__':
    multiprocessing.log_to_stderr(logging.DEBUG)
    try:
        with open(settings) as settings_file:
            sensor_settings = json.load(settings_file)
    except IOError:
        raise IOError('Settings file not found: {}. Set the environment variable MINION_SETTINGS to the correct path'.format(settings))

    # Ativate the communication system

    # Start all the sensors
    sensor_processes = []
    logger = multiprocessing.get_logger()
    for sensor_details in sensor_settings.get('sensors', []):
        sensor_class = minion.utils.module_loading.import_string(sensor_details['class'])

        # instantiate
        sensor = sensor_class(**sensor_details)

        d = multiprocessing.Process(name=sensor_details['name'], target=sensor.run)

        d.start()

        d.join(100000000)
