import minion.acting.base
import multiprocessing
import subprocess
import threading

logger = multiprocessing.get_logger()

def say_it(self, *args):
    voice = ''
    if 'voice' in self.configuration:
        voice = ' -v "{}" '.format(self.configuration['voice'])
    subprocess.call('say {voice} {what_to_say}'.format(what_to_say=args[0], voice=voice), shell=True)

class SimpleSay(minion.acting.base.BaseActuator):
    def act(self, *args, **kwargs):
        t = threading.Thread(target=say_it, args=(self,)+args)
        t.start()
