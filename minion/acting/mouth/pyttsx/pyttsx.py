import minion.acting.base
import minion.core.utils.functions
import multiprocessing
import pyttsx
import threading

logger = multiprocessing.get_logger()


class SimpleSay(minion.acting.base.BaseActuator):
    def say(self, *args):
        engine = pyttsx.init()
        voice_id = self._get_voice()
        if voice_id is not None:
            engine.setProperty('voice', voice_id)

        engine.setProperty('rate', self._get_rate())

        for sentence in args:
            engine.say(args)

        engine.runAndWait()

    @minion.core.utils.functions.configuration_getter
    def _get_voice(self):
        return None

    @minion.core.utils.functions.configuration_getter
    def _get_rate(self):
        return 150

    def act(self, *args, **kwargs):
        t = threading.Thread(target=super(SimpleSay, self).say, args=args)
        t.start()
