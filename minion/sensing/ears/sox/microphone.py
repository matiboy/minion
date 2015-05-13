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

    def _get_tempfile_suffix(self):
        return '.{}'.format(self.configuration['format'])

    def sense(self):
        with tempfile.NamedTemporaryFile(suffix=self._get_tempfile_suffix()) as audio_temporary_file:
            logger.debug(audio_temporary_file.name)
            subprocess.call(self._build_sox_command(audio_temporary_file), shell=True)
            audio_data = audio_temporary_file.read()
            return audio_data

    def _build_sox_command(self, filename):
        raise NotImplementedError('_build_sox_command needs to be implemented in MicrophoneListener subclasses')


class MicrophoneSelectiveListener(MicrophoneListener):
    configuration = {
        'format': 'flac',
        'rate': '16000',
        'silence_pre_level': '4%',
        'silence_pre_trim': 1,
        'silence_pre_duration': 0.5,
        'silence_post_level': '4%',
        'silence_post_trim': 0,
        'silence_post_duration': 0.8,
        # Options are the "-" options for the shell
        'options': {
            'c': 1,
            'b': 16
        }
    }
    period = 0.1

    def _update_configuration(self, configuration):
        """
            Extends default configuration update function
            For readability purposes, configuration of silence values is set as an object as seen below
            ```
                "configuration": {
                    "format": "wav",
                    "silence": {
                        "pre": {
                            "level": "10%",
                            "trim": 1,
                            "duration": 0.05
                        },
                        "post": {
                            "level": "10%",
                            "trim": 1,
                            "duration": 0.8
                        }
                    }
                }
            ```
            Also the "options" object will be converted to a string e.g.
            ```
            {
                "c": 1,
                "d": 16
            }
            ```
            will become "-c 1 -d 16"
        """
        super(MicrophoneSelectiveListener, self)._update_configuration(configuration)
        options = ['-{} {}'.format(key, value) for key, value in self.get_configuration('options', {}).iteritems()]
        self._configuration['options'] = ' '.join(options)

        if 'silence' in configuration:
            silence = configuration['silence']
            for when in ('pre', 'post'):
                if when in silence:
                    when_config = silence[when]
                    for what in ('level', 'trim', 'duration'):
                        if what in when_config:
                            self._configuration['silence_{}_{}'.format(when, what)] = when_config[what]

    def _build_sox_command(self, f):
        command = '/usr/bin/rec {options} {tempfile} rate {rate} silence {silence_pre_trim} {silence_pre_duration} {silence_pre_level} {silence_post_trim} {silence_post_duration} {silence_post_level}'.format(tempfile=f.name, **self._configuration)
        logger.debug(command)
        return command
