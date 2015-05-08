import minion.acting.base
import multiprocessing
import subprocess

logger = multiprocessing.get_logger()


class SimpleSay(minion.acting.base.BaseActuator):
    configuration = {}

    def act(self, *args, **kwargs):
        voice = ''
        if 'voice' in self.configuration:
            voice = ' -v "{}" '.format(self.configuration['voice'])
        subprocess.call('say {voice} {what_to_say}'.format(what_to_say=args[0], voice=voice), shell=True)
