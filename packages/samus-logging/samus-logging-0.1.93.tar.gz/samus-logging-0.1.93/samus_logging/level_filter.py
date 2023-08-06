import logging


class LevelFilter(logging.Filter):
    """Filters Messages below to given Level (as Integer). \n
    (based on https://stackoverflow.com/a/7447596/190597)
    """
    level = None

    def __init__(self, level=0):
        """Creates Filter. \n
        - level: filter out Messages below to given Level (as Integer)
        """
        super().__init__()
        self.level = level

    def filter(self, message) -> int:
        return message.levelno >= self.level
