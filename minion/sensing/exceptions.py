class DataUnavailable(Exception):
    """Used when no new data is available"""
    pass


class DataReadError(Exception):
    """Raise if an error occured while reading the data"""
    pass
