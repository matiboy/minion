from . import errors
import time
import multiprocessing
import minion.utils.module_loading
import threading

logger = multiprocessing.get_logger()


class BaseSensor(object):
    active = True

    def __init__(self, nervous_system, configuration={}, preprocessors=[], postprocessors=[], **kwargs):
        self.name = configuration.get('name', 'anonymous')
        self.nervous_system = nervous_system
        processors = []
        for p in postprocessors:
            try:
                c = minion.utils.module_loading.import_string(p['class'])
            except ImportError:
                logger.critical('Unable to import {}'.format(p['class']))
            else:
                processors.append(c(configuration=p.get('configuration', {})))

        self.postprocessors = processors

        self.preprocessors = preprocessors

        # Try updating configuration if it exists on the class
        try:
            self.configuration.update(configuration)
        except AttributeError:
            self.configuration = configuration

        try:
            self._validate_configuration()
        except errors.ImproperlyConfigured as e:
            raise errors.ImproperlyConfigured('Sensor <%s> has invalid configuration: %s', self.name, e)
        logger.info('Sensor <%s> created with configuration %s', self.name, self.configuration)

    def _validate_configuration(self):
        return

    def is_active(self):
        # Run all the preprocessors of type ActiveStatePreprocessor
        for p in self.preprocessors:
            print p
        return self.active

    def run(self):
        data = self.sense()
        self.post_process(data)
        return

    # Publish channel override
    # By defaut, leaves it to the nervous system to decide which channel messages are sent on
    def _get_publish_channel(self):
        return None

    def post_process(self, data):
        logger.debug('Sensor data received, preparing to post process')
        for p in self.postprocessors:
            logger.debug(p)
            data = p.process(data)

        # Use nervous system to pass on data
        self.nervous_system.publish(channel=self._get_publish_channel(), message=data)

    def sense(self):
        raise NotImplementedError('Sense method needs to be implemented on sensor')


class AlwaysOnSensor(object):
    def is_active(self):
        return True


class ContinuousSensor(BaseSensor):
    # Key that the constructor will look for either on the class or in the configuration
    period_attribute = 'period'

    def __init__(self, nervous_system, configuration={}, preprocessors=[], postprocessors=[], **kwargs):
        super(ContinuousSensor, self).__init__(nervous_system, configuration, preprocessors, postprocessors, **kwargs)
        # Make sure we have a period
        if not hasattr(self, self.period_attribute) and self.period_attribute not in configuration:
            raise errors.ImproperlyConfigured('Continous sensor requires a sensing period')
        # Keep the period
        if self.period_attribute in configuration:
            self.period = configuration[self.period_attribute]
        logger.debug('Creating continuous sensor <%s> with period %s', self.name, self.period)

    def run(self):
        while self.is_active():
            try:
                data = self.sense()
            except errors.DataUnavailable:
                pass
            else:
                threading.Thread(target=self.post_process, args=(data,)).start()
            time.sleep(self.period)
