import subprocess
import minion.postprocessors


class GoogleSpeechToText(minion.postprocessors.BasePostprocessor):
    configuration = {
        'url': 'http://www.google.com/speech-api/v2/recognize',
        'lang': 'en-us',
        'client': 'chromium'
    }

    def process(self, data):
        # Write to a temporary file
        # TODO see if we can avoid the temp file
        file_format = '.{}'.format(self.configuration['type'])
        with tempfile.NamedTemporaryFile(suffix=file_format) as original_file:
            out = subprocess.check_output('/usr/bin/soxi -D {}'.format(original_file.name))
            try:
                duration = float(out)
            # TODO What exceptions do we expect?
            except:
                return data
            else:
                # Check if audio is too long
                if not self._is_too_long(duration):
                    return data

                with tempfile.NamedTemporaryFile(suffix=file_format) as reduced_file:
                    subprocess.call(self._build_sox_call(duration, original_file, reduced_file), shell=True)
                    return reduced_file.read()

    def _build_sox_call(duration, original, target):
        return '/usr/bin/sox {} {} trim {} {}'.format(original.name, target.name, duration, duration+1)
