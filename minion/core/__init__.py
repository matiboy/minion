from .components import exceptions
import minion.core.utils.module_loading
import multiprocessing
import time

logger = multiprocessing.get_logger()


class Minion(object):
    loop_period = 0.1

    def __init__(self):
        self.sensors = {}
        self.actuators = {}
        self.commands = {}

    def attach_nervous_system(self, configuration):
        if 'name' not in configuration:
            raise exceptions.ImproperlyConfigured('Name is required for nervous system')

        nervous_system_class = minion.core.utils.module_loading.import_string(configuration['class'])
        self.nervous_system = nervous_system_class(**configuration)

    def _get_classes(self, *objects):
        classes = []
        for object_details in objects:
            # Names should be different for all objects
            name = object_details['name']
            # Remove so it doesn't cause problems in kwargs
            # FIXME there has to be a cleaner way
            del object_details['name']
            object_class = minion.core.utils.module_loading.import_string(object_details['class'])
            del object_details['class']
            if 'configuration' not in object_details:
                object_details['configuration'] = {}
            classes.append((name, object_class, object_details))

        return classes

    def attach_sensors(self, *sensors):
        classes = self._get_classes(*sensors)

        for name, object_class, object_details in classes:
            if name in self.sensors:
                raise exceptions.NameConflict('Sensor name <{}> is already in use'.format(name))

            sensor = object_class(name, self.nervous_system, **object_details)

            self.sensors[name] = sensor

    def attach_actuators(self, *actuators):
        classes = self._get_classes(*actuators)
        for name, object_class, object_details in classes:
            if name in self.actuators:
                raise exceptions.NameConflict('Actuator name <{}> is already in use'.format(name))

            actuator = object_class(name, **object_details)

            self.actuators[name] = actuator

    def attach_commands(self, *commands):
        classes = self._get_classes(*commands)
        for name, object_class, object_details in classes:
            if name in self.commands:
                raise exceptions.NameConflict('Command name <{}> is already in use'.format(name))

            command = object_class(name, object_details['configuration'])

            self.commands[name] = command

    def _gather_channels(self):
        publish_channels = set()
        # Nervous system publishing command
        publish_channels.add(self.nervous_system.channel)

        # Gather from sensors
        for sensor in self.get_sensors():
            sensor_channel = sensor.get_publish_channel()
            if sensor_channel is not None:
                publish_channels.add(sensor_channel)

        actuator_channels = set()
        for actuator in self.get_actuators():
            actuator_channels.update(actuator.channels)

        return publish_channels, actuator_channels

    def get_sensors(self):
        return self.sensors.values()

    def get_commands(self):
        return self.commands.values()

    def get_actuators(self):
        return self.actuators.values()

    def loop(self):
        # Gather channels that nervous system needs to listen on
        command_channels, actuator_channels = self._gather_channels()
        all_channels = command_channels.union(actuator_channels)
        # Tell the nervous system to subscribe to these channels
        self.nervous_system.subscribe(*all_channels)

        for sensor_name, sensor in self.sensors.iteritems():
            p = multiprocessing.Process(name=sensor_name, target=sensor.run)
            p.start()

        while True:
            for m in self.nervous_system.listen():
                logger.debug('Command received: %s', m)
                command = m.get_message()
                channel = m.get_channel()

                # Differentiate between command/action channels
                if channel in command_channels:
                    for c in self.get_commands():
                        try:
                            command_details = c.matches(command)
                        except minion.understanding.exceptions.DoesNotMatch:
                            continue

                        logger.debug('Command <%s> can handle command %s', c, command)
                        c.understand(self.nervous_system, command, *command_details)

                elif channel in actuator_channels:
                    for actuator in self.get_actuators():
                        if actuator.can_handle(m.get_channel()):
                            actuator.act(m.get_message())
                else:
                    logger.info('Message got lost in translation: %s', m)

            time.sleep(self.loop_period)
