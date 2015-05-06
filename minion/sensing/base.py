from . import errors
import time
import multiprocessing
import minion.utils.module_loading

logger = multiprocessing.get_logger()


class BaseSensor(object):
    active = True

    def __init__(self, configuration={}, preprocessors=[], postprocessors=[], **kwargs):
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

    def is_active(self):
        # Run all the preprocessors of type ActiveStatePreprocessor
        for p in self.preprocessors:
            print p
        return self.active

    def run(self):
        data = self.sense()
        self.post_process(data)
        return

    def post_process(self, data):
        for p in self.postprocessors:
            logger.debug(p)
            data = p.process(data)
        return data

    def sense(self):
        raise NotImplementedError('Sense method needs to be implemented on sensor')

class AlwaysOnSensor(object):
    def is_active(self):
        return True

class ContinuousSensor(BaseSensor):
    def __init__(self, configuration={}, preprocessors=[], postprocessors=[], **kwargs):
        super(ContinuousSensor, self).__init__(configuration, preprocessors, postprocessors, **kwargs)
        # Make sure we have a period
        if not hasattr(self, 'period') and not configuration.get('period'):
            raise errors.ImproperlyConfigured('Continous sensor requires a sensing period')

    def run(self):
        while self.is_active():
            try:
                data = self.sense()
            except errors.DataUnavailable:
                pass
            else:
                self.post_process(data)
            time.sleep(self.period)
