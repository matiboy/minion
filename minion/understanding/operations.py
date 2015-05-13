class UnderstandingOperation(object):
    """
    Base command object that can also be used as an iterator (which will return itself only)
    This means that Command objects' understand methods can return either a list of such objects, and a single instance of it
    """
    _used = False

    def __init__(self, action, message):
        self.action = action
        self.message = message

    def __iter__(self):
        return self

    def next(self):
        if not self._used:
            self._used = True
            return self

        raise StopIteration

    def publish(self, nervous_system):
        nervous_system.publish(self.action, self.message)


class Noop(object):
    """
    Return an instance of this object when no operation is expected
    """
    def __init__(self, *args, **kwargs):
        pass

    def __iter__(self):
        return self

    def next(self):
        raise StopIteration

    def publish(self, nervous_system):
        pass