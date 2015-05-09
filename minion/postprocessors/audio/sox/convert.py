import subprocess
import tempfile
import minion.postprocessors
import multiprocessing

logger = multiprocessing.get_logger()


class Convert(minion.postprocessors.BasePostprocessor):
    configuration = {
        'format': 'wav'
    }

    def process(self, data):
        # Write to a temporary file
        file_format = '.{}'.format(self.configuration['format'])
        with tempfile.NamedTemporaryFile(suffix=file_format) as original_file:
            with tempfile.NamedTemporaryFile(suffix=file_format, delete=False) as converted_file:
                original_file.write(data)
                options = []
                for o in self.configuration:
                    if o != 'format':
                        options.append('-{} {}'.format(o, self.configuration[o]))

                logger.debug('/usr/bin/sox {original} {options} {converted}'.format(options=' '.join(options), original=original_file.name, converted=converted_file.name))
                subprocess.call('/usr/bin/sox {original} {options} {converted}'.format(options=' '.join(options), original=original_file.name, converted=converted_file.name), shell=True)

                return converted_file.read()
