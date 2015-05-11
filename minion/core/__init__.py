from .components import exceptions
import minion.utils.module_loading
import multiprocessing
import time


class Minion(object):
    loop_period = 0.1

    def __init__(self):
        self.sensors = {}
        self.actuators = {}
        self.commands = {}

    def attach_nervous_system(self, configuration):
        if 'name' not in configuration:
            raise exceptions.ImproperlyConfigured('Name is required for nervous system')

        nervous_system_class = minion.utils.module_loading.import_string(configuration['class'])
        self.nervous_system = nervous_system_class(**configuration)

    def _get_classes(self, *objects):
        classes = []
        for object_details in objects:
            # Names should be different for all objects
            name = object_details['name']
            # Remove so it doesn't cause problems in kwargs
            # FIXME there has to be a cleaner way
            del object_details['name']
            object_class = minion.utils.module_loading.import_string(object_details['class'])
            del object_details['class']
            if 'configuration' not in object_details:
                object_details['configuration'] = {}
            classes.append((name, object_class, object_details))

        return classes

    def attach_sensors(self, *sensors):
        classes = self._get_classes(*sensors)

        for name, object_class, object_details in classes:
            if name in self.sensors:
                raise exceptions.NameConflict('Sensor name <%s> is already in use', name)

            sensor = object_class(name, self.nervous_system, **object_details)

            self.sensors[name] = sensor

    def attach_actuators(self, *actuators):
        classes = self._get_classes(*actuators)
        for name, object_class, object_details in classes:
            if name in self.actuators:
                raise exceptions.NameConflict('Actuator name <%s> is already in use', name)
            print object_details
            actuator = object_class(name, **object_details)

            self.actuators[name] = actuator

    def attach_commands(self, *commands):
        return self._attach('commands', False, *commands)

    def loop(self):
        # Gather channels that nervous system needs to listen on
        # TODO

        for sensor_name, sensor in self.sensors.iteritems():
            p = multiprocessing.Process(name=sensor_name, target=sensor.run)
            p.start()

        while True:

            time.sleep(self.loop_period)
