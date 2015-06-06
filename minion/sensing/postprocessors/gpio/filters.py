import minion.sensing.postprocessors
import minion.sensing.exceptions
import minion.core.components.exceptions
import minion.core.utils.functions
import multiprocessing

logger = multiprocessing.get_logger()


class GpioPostprocessor(minion.sensing.postprocessors.BasePostprocessor):
    def validate_raw_date(self, data):
        # We're expecting data to contain new and old values
        try:
            new_value, old_value = data
        except ValueError:
            raise minion.sensing.exceptions.DataReadError('Expecting new and old values, got {}'.format(data))        
        
        return new_value, old_value

class ChangeOnly(GpioPostprocessor):
    def process(self, data):
        new_value, old_value = self.validate_raw_data(data)

        if new_value == old_value:
            raise minion.sensing.exceptions.DataUnavailable

        # Simply pass through since we detected a change
        return data


class HighOnly(GpioPostprocessor):
    def process(self, data):
        new_value, old_value = self.validate_raw_data(data)

        # We only care about new value
        if new_value == 0:
            raise minion.sensing.exceptions.DataUnavailable

        # Simply pass through since we detected a high
        return data


class LowOnly(GpioPostprocessor):
    def process(self, data):
        new_value, old_value = self.validate_raw_data(data)

        # We only care about new value
        if new_value == 1:
            raise minion.sensing.exceptions.DataUnavailable

        # Simply pass through since we detected a low
        return data
