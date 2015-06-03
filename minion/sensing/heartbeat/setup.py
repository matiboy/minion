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
            'name': 'Heartbeat',
            'class': 'minion.sensing.heartbear.beat.Heartbeat',
            'description': '''
<h3>Repeats a simple command at given intervals</h3>
<h4>Output: command</h4>
<p>Used mostly for debugging purposes</p>
            ''',
            'setup': [{
                'type': 'input',
                'name': 'message',
                'default': 'say hi',
                'message': 'Message to output at regular interval'
            },
            {
                'type': 'input',
                'name': 'period',
                'default': '30',
                'message': 'Period to repeat command in seconds'
            }],
            'requirements': (),
        }
    ]
}
