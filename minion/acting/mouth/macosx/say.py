import minion.acting.base
import multiprocessing
import threading

logger = multiprocessing.get_logger()


class SimpleSay(minion.acting.base.ShellCommandActuator):
    def _build_command(self, *args, **kwargs):
        # Transform pauses
        to_say = args[0].replace('$$pause$$', '[[slnc 2000]]').replace('$$longpause$$', '[[slnc 5000]]')
        # TODO This is rather ugly
        voice = self.get_configuration('voice', [])
        if voice.__len__():
            voice = ['-v', voice]
            return ['say'] + voice + [to_say]

    def act(self, *args, **kwargs):
        t = threading.Thread(target=super(SimpleSay, self).act, args=args)
        t.start()
