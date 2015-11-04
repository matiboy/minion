from . import exceptions
import minion.core.components
import minion.core.utils.functions
import minion.core.utils.module_loading
import minion.preprocessors.exceptions
import minion.sensing.exceptions
import multiprocessing
import threading
import time

logger = multiprocessing.get_logger()


class BaseSensor(minion.core.components.NervousComponent):
    active = True

    def __init__(self, name, nervous_system, configuration={}, preprocessors=[], postprocessors=[], **kwargs):
        super(BaseSensor, self).__init__(name, nervous_system, configuration)

        self.nervous_system = nervous_system
        processors = []
        for p in postprocessors:
            try:
                c = minion.core.utils.module_loading.import_string(p['class'])
            except ImportError:
                logger.critical('Unable to import {}'.format(p['class']))
            else:
                processors.append(c(p.get('name', ''), configuration=p.get('configuration', {})))

        self.postprocessors = processors

        processors = []
        for p in preprocessors:
            try:
                c = minion.core.utils.module_loading.import_string(p['class'])
            except ImportError:
                logger.critical('Unable to import {}'.format(p['class']))
            else:
                processors.append(c(p.get('configuration', {})))

        self.preprocessors = processors

        # TODO Check whether this is still needed. Doesn't the base component do all this?
        # Try updating configuration if it exists on the class
        try:
            self.configuration = self.configuration.copy()
            self.configuration.update(configuration)
        except AttributeError:
            self.configuration = configuration

        try:
            self._validate_configuration()
        except exceptions.ImproperlyConfigured as e:
            raise exceptions.ImproperlyConfigured('Sensor <%s> has invalid configuration: %s', self.name, e)
        logger.info('Sensor <%s> created with configuration %s', self.name, self._configuration)

    def _validate_configuration(self):
        return

    def is_active(self):
        # Run all the preprocessors
        go_ahead = True
        for p in self.preprocessors:
            try:
                p.test()
            except minion.preprocessors.exceptions.StopProcess:
                go_ahead = False
                break
            except minion.preprocessors.exceptions.ProcessValid:
                # Means we can go ahead without checking other preprocessors
                break
        return go_ahead

    def run(self):
        if self.is_active():
            data = self.sense()
            self.post_process(data)
        return

    @minion.core.utils.functions.configuration_getter
    def get_publish_channel(self):
        """
            Publish channel override
            By defaut, leaves it to the nervous system to decide which channel messages are sent on
        """
        return None

    def post_process(self, data):
        logger.debug('Sensor data received, preparing to post process')
        for p in self.postprocessors:
            try:
                data = p.process(data)
            except minion.sensing.exceptions.DataUnavailable:
                return

        # Use nervous system to pass on data
        self.publish_on_nervous_system(data)

    def publish_on_nervous_system(self, data):
        """
        Publishes onto the nervous system to a default channel
        """
        self.nervous_system.publish(channel=self.get_publish_channel(), message=data)

    def sense(self):
        raise NotImplementedError('Sense method needs to be implemented on sensor')


class ContinuousSensor(BaseSensor):
    def __init__(self, name, nervous_system, configuration={}, preprocessors=[], postprocessors=[], **kwargs):
        super(ContinuousSensor, self).__init__(name, nervous_system, configuration, preprocessors, postprocessors, **kwargs)
        logger.debug('Creating continuous sensor <%s> with period %s', self.name, self._get_period())

    @minion.core.utils.functions.configuration_getter
    def _get_period(self):
        """Configuration getter that falls back to class value or 0 if all that failed"""
        try:
            # Could be class level
            return self.period
        except AttributeError:
            # Defaut to immediate?
            return 0

    @minion.core.utils.functions.configuration_getter
    def _get_immediate(self):
        return True

    def _get_inactive_period(self):
        """
        Returns the second value of period if it is an array, the get_value period otherwise
        Parses to a float; raises if invalid value
        """
        period = self._get_period()
        # Might have a list of 2 items
        try:
            _, inactive = period
        except (TypeError, ValueError):
            inactive = period
        return float(inactive)

    def _get_active_period(self):
        period = self._get_period()
        # Might have a list of 2 items
        try:
            active, _ = period
        except (TypeError, ValueError):
            active = period
        return float(active)

    def run(self):
        immediate = self._get_immediate()
        while True:
            is_active = self.is_active()
            # Waiting period depends on active or not (if 2 values are provided)
            if is_active:
                period = self._get_active_period()
            else:
                period = self._get_inactive_period()

            # Sensor might not be active
            if not immediate:
                time.sleep(period)

            if is_active:
                try:
                    data = self.sense()
                except exceptions.DataUnavailable:
                    pass
                else:
                    threading.Thread(target=self.post_process, args=(data,)).start()

            # Pause after
            if immediate:
                time.sleep(period)
