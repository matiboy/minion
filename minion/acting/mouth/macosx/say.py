import minion.acting.base
import multiprocessing
import threading

logger = multiprocessing.get_logger()


class SimpleSay(minion.acting.base.ShellCommandActuator):
    def _build_command(self, *args, **kwargs):
        # TODO This is rather ugly
        voice = self.get_configuration('voice', [])
        if voice.__len__():
            voice = ['-v', voice]
            return ['say'] + voice + [args[0]]

    def act(self, *args, **kwargs):
        t = threading.Thread(target=super(SimpleSay, self).act, args=args)
        t.start()
