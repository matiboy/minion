import subprocess
import tempfile
import minion.sensing.exceptions
import minion.sensing.postprocessors
import minion.core.components.exceptions
import multiprocessing

logger = multiprocessing.get_logger()


class PocketsphinxSpeechToText(minion.sensing.postprocessors.BasePostprocessor):
    configuration = {
        'delete_audio_file': True  # Set this to false to debug by keeping audio file after request
    }

    def __init__(self, name, configuration={}):
        super(PocketsphinxSpeechToText, self).__init__(name, configuration)

        options = self.get_configuration('options', {})
        self.options = ' '.join(['-{} {}'.format(key, value) for key, value in options.iteritems()])

    def process(self, data):
        with tempfile.NamedTemporaryFile(delete=self.get_configuration('delete_audio_file')) as f:
            f.write(data)
            logger.debug('Writing to temporary file %s', f.name)
            if not self.get_configuration('delete_audio_file'):
                logger.debug('File will be kept after post-process')

            # TODO Manage to use python pocketsphinx
            command = 'pocketsphinx_continuous -infile {filename} {options}'.format(filename=f.name, options=self.options)
            try:
                out = subprocess.check_output(command, shell=True)
            except subprocess.CalledProcessError as e:
                logger.error('Exit error %s', e)
                raise minion.sensing.exceptions.DataReadError
            except Exception as e:
                logger.error('Unexpected error %s', e)
            else:
                logger.debug(out)
                if out:
                    return out
                else:
                    raise minion.sensing.exceptions.DataUnavailable
