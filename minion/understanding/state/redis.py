from . import base
import redis


class RedisState(base.BaseState):
    configuration = {
        'host': 'localhost',
        'port': 6379,
        'db': 0,
        'name': 'something'
        'expressions': ['set {name} to ']
    }

    def __init__(self, configuration={}):
        self.configuration = self.configuration.copy()
        self.configuration.update(configuration)