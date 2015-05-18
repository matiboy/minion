import inquirer
import minion.core.components


def _prepare_google_stt_config(answers, component):
    answers['postprocessors'] = [
        {
            "configuration": {
                "type": "flac",
                "maxlength": answers['limit_duration']
            },
            "name": "Duration limit",
            "class": "minion.sensing.postprocessors.audio.sox.durationlimit.DurationLimit"
        },
        {
            "name": "Google Speech to text",
            "class": "minion.sensing.postprocessors.audio.google.speechtotext.GoogleSpeechToText",
            "configuration": {
                "API_KEY": [answers['api_key']]
            }
        }
    ]
    del answers['api_key']
    del answers['limit_duration']
    answers['format'] = 'flac'
    answers['options'] = {
        'c': 1,
        'b': 16
    }
    return answers


def _prepare_google_apiai_config(answers, component):
    answers['postprocessors'] = [
        {
            "configuration": {
                "type": "wav",
                "maxlength": answers['limit_duration']
            },
            "name": "Duration limit",
            "class": "minion.sensing.postprocessors.audio.sox.durationlimit.DurationLimit"
        },
        {
            "name": "API.ai Speech to text",
            "class": "minion.sensing.postprocessors.audio.apiai.speechtotext.ApiaiSpeechToText",
            "configuration": {
                "SUBSCRIBTION_KEY": answers['SUBSCRIBTION_KEY'],
                "CLIENT_ACCESS_TOKEN": answers['CLIENT_ACCESS_TOKEN']
            }
        }
    ]
    del answers['SUBSCRIBTION_KEY']
    del answers['CLIENT_ACCESS_TOKEN']
    del answers['limit_duration']
    answers['format'] = 'wav'
    answers['options'] = {
        'c': 1,
        'b': 16
    }

    return answers

defines = {
    minion.core.components.Types.SENSOR: [
        {
            'name': 'Always listening microphone with silence detection - Google STT',
            'class': 'minion.sensing.ears.sox.microphone.MicrophoneSelectiveListener',
            'questions': [
                inquirer.Text('rate', message='Recording rate (Hz)', default='16000'),
                inquirer.Text('silence_pre_level', message='Level of silence before recording (%)', default='10%'),
                inquirer.Text('silence_pre_duration', message='Duration of noise before recording (seconds)', default='0.5'),
                inquirer.Text('silence_post_level', message='Level of silence before stop recording (%)', default='10%'),
                inquirer.Text('silence_post_duration', message='Duration of silence to stop recording (seconds)', default='0.8'),
                inquirer.Text('api_key', message='Google API key'),
                inquirer.Text('limit_duration', message='Reduce recording before sending to API to how many seconds?', default=10)
            ],
            'description': '''
# Uses SOX to record constantly via the microphone.
# Starts recording when there is sufficient noise (silence_pre_level) for a sufficient duration (silence_pre_duration)
# Stops recording when there is a long enough silence (below silence_post_level for at least silence_post_duration seconds)
#
# Then uses Google Speech API to translate to a string
# Refer to http://stackoverflow.com/questions/26485531/google-speech-api-v2 to get an API key
#
# Requires SOX to be installed
            ''',
            'requirements': (
                'pysox',
            ),
            'process_answers': _prepare_google_stt_config
        },
        {
            'name': 'Always listening microphone with silence detection - Api.ai STT',
            'class': 'minion.sensing.ears.sox.microphone.MicrophoneSelectiveListener',
            'questions': [
                inquirer.Text('rate', message='Recording rate (Hz)', default='16000'),
                inquirer.Text('silence_pre_level', message='Level of silence before recording (%)', default='10%'),
                inquirer.Text('silence_pre_duration', message='Duration of noise before recording (seconds)', default='0.5'),
                inquirer.Text('silence_post_level', message='Level of silence before stop recording (%)', default='10%'),
                inquirer.Text('silence_post_duration', message='Duration of silence to stop recording (seconds)', default='0.8'),
                inquirer.Text('SUBSCRIBTION_KEY', message='Subscription key'),
                inquirer.Text('CLIENT_ACCESS_TOKEN', message='Client access token'),
                inquirer.Text('limit_duration', message='Reduce recording before sending to API to how many seconds?', default=10)
            ],
            'description': '''
# Uses SOX to record constantly via the microphone.
# Starts recording when there is sufficient noise (silence_pre_level) for a sufficient duration (silence_pre_duration)
# Stops recording when there is a long enough silence (below silence_post_level for at least silence_post_duration seconds)
#
# Then uses API.ai to translate to a string
# Refer to http://api.ai to get an access token
#
# Requires SOX to be installed
            ''',
            'requirements': (
                'pysox',
            ),
            'process_answers': _prepare_google_apiai_config
        }
    ]
}
