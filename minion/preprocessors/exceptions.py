class StopProcess(Exception):
    """Raised when a pre processor fails and decides to stop other processors"""
    pass


class ProcessValid(Exception):
    """Raised when a pre processor succeeds and decides there is no need for other processors"""
    pass
