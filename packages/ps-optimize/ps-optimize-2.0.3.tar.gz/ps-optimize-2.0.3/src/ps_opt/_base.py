from datetime import datetime


class _Base:
    """
    Class '_Base' consist of a single method '_system_datetime',
    and takes no arguments to instantiate.
    """
    def __init__(self):
        pass

    @property
    def _system_datetime(self):
        """
        return current datetime in '[%Y-%m-%d | %H:%M:%S]' format.
        This method is primarily used for constructing message to
        inform users which stage is the feature selection currently
        at.
        """
        return datetime.now().strftime("[%Y-%m-%d | %H:%M:%S]")
