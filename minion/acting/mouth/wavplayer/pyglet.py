import minion.acting.base
import multiprocessing
import pyglet

logger = multiprocessing.get_logger()


class PygletPlayer(minion.acting.base.BaseActuator):
    def act(self, *args, **kwargs):
        # TODO allow for binary data as well as file names
        logger.debug('Playing sounds %s via Pyglet', ', '.join(args))
        for f in args:
            sound = pyglet.media.load(f, streaming=False)
            # TODO Check that this doesn't open in a new thread
            sound.play()
