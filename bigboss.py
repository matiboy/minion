import flask
import boss.settings
import boss.utils.auth
import json
import minion.core.utils.console
import minion.core.configure
import minion.core.components

simple_page = flask.Blueprint('simple_page', __name__, template_folder='boss/templates', static_folder='boss/static', static_url_path='/static/boss')
app = flask.Flask(__name__)
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')


@app.before_request
def before_request():
    flask.g.settings = boss.settings.load_settings()


@simple_page.route('/')
@boss.utils.auth.requires_auth
def dashboard():
    settings = flask.g.settings
    return flask.render_template('dashboard.jade',
        has_nervous_system=settings['nerve'],
        sensors_count=settings['sensors'].__len__(),
        actuators_count=settings['actuators'].__len__(),
        commands_count=settings['commands'].__len__()
        )


@simple_page.route('/save_nerve', methods=['POST'])
@boss.utils.auth.requires_auth
def save_nerve():
    setup = flask.request.get_json()
    boss.settings.save('nerve', setup)

    return flask.jsonify(status=0)


@simple_page.route('/nerve')
@boss.utils.auth.requires_auth
def nerve():
    modules = minion.core.configure.modules
    settings = flask.g.settings
    return flask.render_template('nerve.jade',
        nervous_system=json.dumps(settings['nerve']),
        available_nerves=json.dumps(modules[minion.core.components.Types.NERVOUS_SYSTEM]),
        systems=modules[minion.core.components.Types.NERVOUS_SYSTEM]
        )


@simple_page.route('/save_object/<component_type>', methods=['POST'])
@boss.utils.auth.requires_auth
def save_object(component_type):
    setup = flask.request.get_json()
    components = flask.g.settings.get(component_type, [])
    # Remove unwanted stuff if need be, this will also help us find out create vs edit
    try:
        index = setup['index']
        del setup['index']
    except KeyError:
        components.append(setup)
    else:
        index = int(index) - 1
        components[index] = setup

    boss.settings.save(component_type, components)

    return flask.jsonify(status=0)


@simple_page.route('/remove_object/<component_type>/<index>', methods=['POST'])
@boss.utils.auth.requires_auth
def remove_object(component_type, index):
    current_settings = flask.g.settings[component_type]

    # 1-based index for readability, to be reconsidered
    index = int(index) - 1
    current_settings.pop(index)

    boss.settings.save(component_type, current_settings)

    return flask.redirect(flask.url_for('simple_page.{}'.format(component_type)))


@simple_page.route('/components/<component_type>')
@boss.utils.auth.requires_auth
def component_list(component_type):
    items = flask.g.settings.get(component_type, [])
    for i, x in enumerate(items):
        x['index'] = i+1
    return flask.render_template('{}.jade'.format(component_type),
        items=items,
        component_type=component_type
        )


@simple_page.route('/components/<component_type>/<index>')
@simple_page.route('/components/<component_type>/create', defaults={'index': -1})
@boss.utils.auth.requires_auth
def edit_object(component_type, index):
    settings = flask.g.settings
    if index == -1:
        obj = {}
        editing = False
    else:
        index = int(index)
        obj = settings[component_type][index-1]
        obj['index'] = index
        editing = True

    return globals()['edit_{}'.format(component_type)](obj, index, editing)


def edit_actuators(obj, index, editing):
    modules = minion.core.configure.modules
    return flask.render_template('actuator.jade',
        index=index,
        actuator=json.dumps(obj),
        available_actuators=json.dumps(modules[minion.core.components.Types.ACTUATOR]),
        editing=editing,
        systems=modules[minion.core.components.Types.ACTUATOR],
        available_preprocessors=json.dumps(modules[minion.core.components.Types.PRE_PROCESSOR]),
        preprocessors=modules[minion.core.components.Types.PRE_PROCESSOR],
        )


def edit_sensors(obj, index, editing):
    modules = minion.core.configure.modules
    return flask.render_template('sensor.jade',
        index=index,
        sensor=json.dumps(obj),
        available_sensors=json.dumps(modules[minion.core.components.Types.SENSOR]),
        editing=editing,
        systems=modules[minion.core.components.Types.SENSOR],
        available_postprocessors=json.dumps(modules[minion.core.components.Types.POST_PROCESSOR]),
        postprocessors=modules[minion.core.components.Types.POST_PROCESSOR],
        )

app.register_blueprint(simple_page)
if __name__ == '__main__':
    minion.core.configure.discover()
    settings = boss.settings.settings
    app.run(debug=settings.get('debug', False), host=settings.get('host', 'localhost'), port=settings.get('port', 5555))
