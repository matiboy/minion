# Copied from http://flask.pocoo.org/snippets/8/
# Credits to Armin Ronacher
from functools import wraps
from flask import request, Response
import boss.settings

try:
    _password = boss.settings.settings['password']
except KeyError:
    raise KeyError('Password key not found in settings file {}'.format(boss.settings.settings))


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == _password


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
