import minion.sensing.postprocessors
import minion.sensing.postprocessors.state.state
import minion.sensing.exceptions
import minion.core.components.exceptions
import minion.core.utils.functions
import multiprocessing

logger = multiprocessing.get_logger()


class ChangeOnly(minion.sensing.postprocessors.state.state.StateChange):
    pass


class HighOnly(minion.sensing.postprocessors.state.state.StateEquals):
    """
    Just a prettier state equals postprocessor with its value preset to 1
    """
    configuration = {
        'value': 1
    }


class LowOnly(minion.sensing.postprocessors.state.state.StateEquals):
    """
    Just a prettier state equals postprocessor with its value preset to 0
    """
    configuration = {
        'value': 0
    }
