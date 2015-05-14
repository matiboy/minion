import subprocess
import tempfile
import minion.sensing.postprocessors
import multiprocessing

logger = multiprocessing.get_logger()


class DurationLimit(minion.sensing.postprocessors.BasePostprocessor):
    configuration = {
        'type': 'flac',
        'maxlength': 10,
        'delete_audio_file': True
    }

    def _is_too_long(self, duration):
        return duration > self.get_configuration('maxlength')

    def process(self, data):
        # Write to a temporary file
        # TODO see if we can avoid the temp file
        file_format = '.{}'.format(self.get_configuration('type'))
        delete = self.get_configuration('delete_audio_file')
        with tempfile.NamedTemporaryFile(suffix=file_format, delete=delete) as original_file:
            original_file.write(data)
            if not delete:
                logger.debug('Original audio file <%s> will be kept after post process', original_file.name)
            logger.debug('Running duration limit command: /usr/bin/soxi -D {}'.format(original_file.name))
            out = subprocess.check_output('/usr/bin/soxi -D {}'.format(original_file.name), shell=True)
            logger.debug(out)
            try:
                duration = float(out)
            # TODO What exceptions do we expect?
            except:
                logger.error('Duration of audio is not a float')
                return data
            else:
                # Check if audio is too long
                if not self._is_too_long(duration):
                    logger.debug('Duration is ok')
                    return data

                with tempfile.NamedTemporaryFile(suffix=file_format, delete=delete) as reduced_file:
                    if not delete:
                        logger.debug('Reduced audio file <%s> will be kept after post process', reduced_file.name)
                    subprocess.call(self._build_sox_call(duration, original_file, reduced_file), shell=True)
                    return reduced_file.read()

    def _build_sox_call(self, duration, original, target):
        return '/usr/bin/sox {} {} trim {} {}'.format(original.name, target.name, duration, duration+1)
