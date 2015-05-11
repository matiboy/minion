from __future__ import absolute_import
import minion.acting.base
import multiprocessing
import pyglet
import time
import threading
import sys

logger = multiprocessing.get_logger()

def blop(f):
    player = pyglet.media.ManagedSoundPlayer()
    sound = pyglet.media.load(f, streaming=False)
    player.queue(sound)
    t = threading.Thread(target=player.play)
    t.start()
    t.join()

class PygletPlayer(minion.acting.base.BaseActuator):
    def __init__(self, name, configuration, channels=[], **kwargs):
        super(PygletPlayer, self).__init__(name, configuration, channels, **kwargs)
        self.channels = channels
        self.player = pyglet.media.Player()
        self.player.eos_action = pyglet.media.Player.EOS_NEXT

    def act(self, *args, **kwargs):
        # TODO allow for binary data as well as file names
        logger.debug('Playing sounds %s via Pyglet', ', '.join(args))
        player = pyglet.media.Player()
        player.queue(*[pyglet.media.load(f, streaming=False) for f in args])
        player.play()
