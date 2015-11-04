class ImproperlyConfigured(Exception):
    """Passed configuration does not match component requirements"""
    pass


class NameConflict(Exception):
    """Name is already in use for this type of component"""
    pass
