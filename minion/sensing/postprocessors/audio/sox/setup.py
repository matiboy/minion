import minion.core.components


defines = {
    minion.core.components.Types.POST_PROCESSOR: [
        {
            'name': 'Sox duration limit',
            'class': 'minion.sensing.postprocessors.sox.durationlimit.DurationLimit',
            'description': '''
<h3>Truncates a recorded audio data to a maximum given duration</h3>
<table class="table table-striped">
    <tr>
        <th>Input</th>
        <th>Output</th>
    <tr>
        <td>Audio data</td>
        <td>Audio data</td>
    </tr>
</table>
<p>Receives audio data from sensor, writes to a temporary file, keep only the last <i>n</i> seconds and the passes audio data back</p>
<p>The temporary file can be kept for debugging by setting the config value <i>delete_audio_file</i> to false</p>
<p><b>IMPORTANT</b> The audio encoding type set in configuration must match the audio type received from the sensor</p>
<p>Requires <a href="http://sox.sourceforge.net/" target="_blank">SOX</a> to be installed</p>
            ''',
            'setup': [{
                'type': 'input',
                'name': 'type',
                'default': 'wav',
                'message': 'Audio encoding'
            },
            {
                'type': 'input',
                'name': 'maxlength',
                'default': '10',
                'message': 'Truncate to last n seconds'
            }],
            'requirements': [],
        }
    ]
}
