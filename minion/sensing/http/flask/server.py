import flask
import minion.core.utils.console
import minion.core.utils.functions
import minion.sensing.base
import multiprocessing
import six
import flask.ext.cors
import json

logger = multiprocessing.get_logger()

class PassthroughEncoder(object):
    def encode(self, data):
        return data

class JSONEncoder(object):
    def encode(self, data):

        return json.dumps(data)

ENCODERS = {
    'passthrough': PassthroughEncoder,
    'json': JSONEncoder
}

class HttpServer(minion.sensing.base.BaseSensor):
    def __init__(self, name, nervous_system, configuration={}, preprocessors=[], postprocessors=[], **kwargs):
        super(HttpServer, self).__init__(name, nervous_system, configuration, preprocessors, postprocessors, **kwargs)
        self.app = self._build_app()
        self.encoder = ENCODERS[self._get_encoder()]()

    @minion.core.utils.functions.configuration_getter
    def _get_encoder(self):
        return 'passthrough'

    @minion.core.utils.functions.configuration_getter
    def _get_route(self):
        return '/banana'

    @minion.core.utils.functions.configuration_getter
    def _get_host(self):
        return '0.0.0.0'

    @minion.core.utils.functions.configuration_getter
    def _get_port(self):
        return 20202

    @minion.core.utils.functions.configuration_getter
    def _get_debug(self):
        return False

    @minion.core.utils.functions.configuration_getter
    def _get_channels(self):
        return []

    @minion.core.utils.functions.configuration_getter
    def _get_allow_cross_origin(self):
        return False

    def get_publish_channel(self, data=None):
        """
        Use channel from POST data if available, leave it to nervous system otherwise

        Data will be None when Minion core is gathering channels to listen to.
        Potential channels should therefore be provided in the configuration otherwise there is a chance that a message will be published but be unheard
        """
        if data is None:
            return self._get_channels()
        # Could be that data is not a dict anymore
        try:
            channel = data.get('channel', None)
        except AttributeError:
            return self._get_channels()
        if channel not in self._get_channels():
            minion.core.utils.console.console_warn('Publish channel <{}> is not in declared channels, message might not be received'.format(channel))
        return channel

    def publish_on_nervous_system(self, data):
        """
        Override default behavior since publish channel will depend on data
        """
        self.nervous_system.publish(channel=self.get_publish_channel(data), message=self.encoder(data))

    def _add_route(self, app, route):
        def r():
            print 'FDSFDSFSD'
            print flask.request.get_json()
            print 'ggfgfgfd'
            data = flask.request.form.copy()
            logger.debug('POST data received: %s', data)
            self.post_process(data)
            return 'Ok'

        app.route(route, methods=["POST"])(r)

    def _build_app(self):
        app = flask.Flask(self.name)
        if self._get_allow_cross_origin():
            flask.ext.cors.CORS(app)
        # Could be a single route
        route = self._get_route()
        print 'route', route
        if isinstance(route, six.string_types):
            self._add_route(app, route)
        else:
            for x in route:
                self._add_route(app, x)

        return app

    def sense(self):
        self.app.run(host=self._get_host(), port=self._get_port(), debug=self._get_debug())


class HttpsServer(HttpServer):
    @minion.core.utils.functions.configuration_getter
    def _get_ssl_certificate(self):
        return 'server.crt'

    @minion.core.utils.functions.configuration_getter
    def _get_ssl_key(self):
        return 'server.key'

    def _get_ssl_context(self):
        return (self._get_ssl_certificate(), self._get_ssl_key(),)

    def sense(self):
        self.app.run(host=self._get_host(), port=self._get_port(), debug=self._get_debug(), ssl_context=self._get_ssl_context())
