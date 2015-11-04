from __future__ import absolute_import
import minion.understanding.base
import minion.understanding.operations
import minion.core.components.exceptions


class MopidyCommand(minion.understanding.base.RedirectCommand):
    configuration = {} # Temporarily needed until we completely move to get_action
    threaded = False

    @minion.core.utils.functions.configuration_getter
    def get_action(self):
        return 'minion:mopidy'


class NextSong(MopidyCommand):
    output = 'next_song'


class PreviousSong(MopidyCommand):
    output = 'previous_song'


class Play(MopidyCommand):
    output = 'play'


class Stop(MopidyCommand):
    output = 'stop'


class ShuffleOn(MopidyCommand):
    output = 'shuffle_on'


class ShuffleOff(MopidyCommand):
    output = 'shuffle_off'


class RepeatOn(MopidyCommand):
    output = 'repeat_on'


class RepeatOff(MopidyCommand):
    output = 'repeat_off'


class VolumeUp(MopidyCommand):
    output = 'volume_up'


class VolumeDown(MopidyCommand):
    output = 'volume_down'


class Mute(MopidyCommand):
    output = 'mute'
