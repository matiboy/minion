import minion.core.components


defines = {
    minion.core.components.Types.POST_PROCESSOR: [
        {
            'name': 'GPIO Change filter',
            'class': 'minion.sensing.postprocessors.gpio.filters.ChangeOnly',
            'description': '''
<h3>GPIO change filter</h3>
<table class="table table-striped">
    <tr>
        <th>Input</th>
        <th>Output</th>
    <tr>
        <td>Tuple(new_value, old_value)</td>
        <td>Tuple(new_value, old_value)</td>
    </tr>
</table>
<h4>Description</h4>
<p>Receives new and old value, only lets things through if there is a change, regardless of new or old value</p>
            ''',
            'setup': [],
            'requirements': [],
        },
        {
            'name': 'GPIO High only filter',
            'class': 'minion.sensing.postprocessors.gpio.filters.HighOnly',
            'description': '''
<h3>GPIO high filter</h3>
<table class="table table-striped">
    <tr>
        <th>Input</th>
        <th>Output</th>
    <tr>
        <td>Tuple(new_value, old_value)</td>
        <td>Tuple(new_value, old_value)</td>
    </tr>
</table>
<h4>Description</h4>
<p>Receives new value (ignores old value), only lets things through if new value is HIGH, regardless of old value</p>
            ''',
            'setup': [],
            'requirements': [],
        },
        {
            'name': 'GPIO Low only filter',
            'class': 'minion.sensing.postprocessors.gpio.filters.LowOnly',
            'description': '''
<h3>GPIO low filter</h3>
<table class="table table-striped">
    <tr>
        <th>Input</th>
        <th>Output</th>
    <tr>
        <td>Tuple(new_value, old_value)</td>
        <td>Tuple(new_value, old_value)</td>
    </tr>
</table>
<h4>Description</h4>
<p>Receives new value (ignores old value), only lets things through if new value is LOW, regardless of old value</p>
            ''',
            'setup': [],
            'requirements': [],
        }
    ]
}
