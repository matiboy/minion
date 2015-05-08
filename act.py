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
            actuators_settings = json.load(settings_file)
    except IOError:
        raise IOError('Settings file not found: {}. Set the environment variable MINION_SETTINGS to the correct path'.format(settings))

    # Ativate the communication system
    try:
        nerve_settings = actuators_settings['nerve']
    except KeyError:
        raise KeyError('You must provide a nervous system')
    nervous_system_class = minion.utils.module_loading.import_string(nerve_settings['class'])
    nervous_system = nervous_system_class(**nerve_settings)

    # Start all the actuators
    logger = multiprocessing.get_logger()

    actuator_instances = []
    for actuator_details in actuators_settings.get('actuators', []):
        actuator_class = minion.utils.module_loading.import_string(actuator_details['class'])

        # instantiate
        actuator = actuator_class(**actuator_details)
        actuator_instances.append(actuator)

    while True:
        for m in nervous_system.listen():
            logger.debug('Command received: %s', m)
            if m['type'] == 'message':
                for actuator in actuator_instances:
                    if actuator.can_handle(m['channel']):
                        d = multiprocessing.Process(name=actuator.name, target=actuator.act, args=(m['data'],))
                        d.start()
