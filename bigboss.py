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

app.register_blueprint(simple_page)
if __name__ == '__main__':
    minion.core.configure.discover()
    settings = boss.settings.settings
    app.run(debug=settings.get('debug', False), host=settings.get('host', 'localhost'), port=settings.get('port', 5555))
