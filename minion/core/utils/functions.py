import functools


def compose(*functions):
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions)


def configuration_getter(default_function):
    """
    Decorator to avoid all the get_configuration methods
    Use _get_<property_name> or get_<property_name> as name of the decorated method
    The decorated method will be used to determine the default value if `property_name` is not present in the configuration dict
    """
    _, _, property_name = default_function.__name__.partition('get_')

    def fn(self):
        return self.get_configuration(property_name, default_function(self))

    return fn
