import inquirer
import minion.core.components


def _prepare_google_stt_config(answers, component):
    print answers

defines = {
    minion.core.components.Types.SENSOR: [
        {
            'name': 'Always listening microphone with silence detection - Google STT',
            'class': 'minion.sensing.ears.sox.microphone.MicrophoneSelectiveListener',
            'questions': [
                inquirer.Text('silence_pre_level', message='Level of silence before recording', default='10%'),
                inquirer.Text('silence_pre_duration', message='Duration of noise before recording', default='0.5'),
                inquirer.Text('silence_post_level', message='Level of silence before stop recording', default='10%'),
                inquirer.Text('silence_post_duration', message='Duration of silence to stop recording', default='0.8'),
                inquirer.Text('api_key', message='Google API key')
            ],
            'requirements': (
                'redis',
            ),
            'process_answers': _prepare_google_stt_config
        }
    ]
}
