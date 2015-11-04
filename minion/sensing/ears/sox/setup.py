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
    return answers

defines = {
    minion.core.components.Types.SENSOR: [
        {
            'name': 'Always listening microphone with silence detection',
            'class': 'minion.sensing.ears.sox.microphone.MicrophoneSelectiveListener',
            'setup': [
                {
                    'name': 'rate',
                    'default': '16000',
                    'type': 'input',
                    'message': 'Recording rate (Hz)'
                },
                {
                    'name': 'silence_pre_level',
                    'default': '10%',
                    'type': 'input',
                    'message': 'Level of silence before recording. Please include the "%" sign'
                },
                {
                    'name': 'silence_pre_duration',
                    'default': '0.1',
                    'type': 'input',
                    'message': 'Duration of noise before recording (seconds)'
                },
                {
                    'name': 'silence_post_level',
                    'default': '10%',
                    'type': 'input',
                    'message': 'Level of silence before stop recording. Please include the "%" sign'
                },
                {
                    'name': 'silence_post_duration',
                    'default': '0.8',
                    'type': 'input',
                    'message': 'Duration of noise before recording (seconds)'
                }
            ],
            'description': '''
<h3>Uses SOX to record constantly via the microphone.</h3>
<h4>Output: Audio data</h4>
<p>Starts recording when there is sufficient noise (<b>silence_pre_level</b>) for a sufficient duration (<b>silence_pre_duration</b>)</p>
<p>Stops recording when there is a long enough silence (below <b>silence_post_level</b> for at least <b>silence_post_duration</b> seconds)</p>
<p>Requires SOX to be installed</p>
<h4>Suggested postprocessors</h4>
<dl>
    <dt>minion.sensing.postprocessors.audio.sox.durationlimit.DurationLimit</dt>
    <dd>Limit duration of recorded audio to a configurable number of seconds</dd>
    <dt>minion.sensing.postprocessors.audio.google.speechtotext.GoogleSpeechToText</dt>
    <dd>Uses Google speech API to translate audio to text</dd>
    <dt>minion.sensing.postprocessors.audio.apiai.speechtotext.ApiaiSpeechToText</dt>
    <dd>Uses Api.ai to translate audio to text</dd>
</dl>
            ''',
            'requirements': (
                'pysox',
            )
        }
    ]
}
#
# Then uses Google Speech API to translate to a string
# Refer to http://stackoverflow.com/questions/26485531/google-speech-api-v2 to get an API key
#
