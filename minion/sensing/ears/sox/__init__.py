import minion.sensing.base
import subprocess
import tempfile
import multiprocessing


logger = multiprocessing.get_logger()

class MicrophoneListener(minion.sensing.base.ContinuousSensor):
    configuration = {
        'format': 'flac',
        'rate': '16000',
        'channels': 1
    }
    def __init__(self, configuration={}, preprocessors=[], postprocessors=[], **kwargs):
        super(MicrophoneListener, self).__init__(configuration, preprocessors, postprocessors, **kwargs)
        self._update_configuration(configuration)

    def _update_configuration(self, configuration):
        self.configuration.update(configuration)

    def _get_tempfile_suffix(self):
        return '.{}'.format(self.configuration['format'])

    def sense(self):
        with tempfile.NamedTemporaryFile(suffix=self._get_tempfile_suffix()) as audio_temporary_file:
            logger.debug(audio_temporary_file.name)
            subprocess.call(self._build_sox_command(audio_temporary_file), shell=True)
            audio_data = audio_temporary_file.read()

    def _build_sox_command(self, filename):
        raise NotImplementedError('_build_sox_command needs to be implemented in MicrophoneListener subclasses')

class MicrophoneSelectiveListener(MicrophoneListener):
    configuration = {
        'format': 'flac',
        'rate': '16000',
        'channels': 1,
        'silence_pre_level': '4%',
        'silence_pre_trim': 1,
        'silence_pre_duration': 0.5,
        'silence_post_level': '4%',
        'silence_post_trim': 0,
        'silence_post_duration': 0.8,
    }
    period = 0.1
    def _update_configuration(self, configuration):
        logger.debug(configuration)
        if 'silence' in configuration:
            silence = configuration['silence']
            logger.debug(silence)
            for when in ('pre', 'post'):
                logger.debug(when)
                if when in silence:
                    when_config = silence[when]
                    logger.debug(when_config)
                    for what in ('level', 'trim', 'duration'):
                        if what in when_config:
                            self.configuration['silence_{}_{}'.format(when, what)] = when_config[what]

        logger.debug(configuration)


    def _build_sox_command(self, f):
        print '/usr/bin/rec -c {channels} {tempfile} rate {rate} silence {silence_pre_trim} {silence_pre_duration} {silence_pre_level} {silence_post_trim} {silence_post_duration} {silence_post_level}'.format(tempfile=f.name, **self.configuration)
        return '/usr/bin/rec -c {channels} {tempfile} rate {rate} silence {silence_pre_trim} {silence_pre_duration} {silence_pre_level} {silence_post_trim} {silence_post_duration} {silence_post_level}'.format(tempfile=f.name, **self.configuration)
