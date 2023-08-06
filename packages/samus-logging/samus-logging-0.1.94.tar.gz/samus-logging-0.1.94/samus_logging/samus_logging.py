import logging
from samus_logging.level_filter import LevelFilter
from pathlib import Path
import os


class Samus_Logging:
    """A minimal Logging-controller."""

    DEFAULT_NAME = 'LOG'
    DEFAULT_LEVEL = 'INFO'
    DEFAULT_LOG_FILE = ''
    DEFAULT_MESSAGE_FORMAT = '%(name)s | %(asctime)s | %(levelname)s | %(filename)s | %(funcName)s() | %(message)s'
    DEFAULT_DATETIME_FORMAT = '%Y.%m.%d %H:%M:%S'
    dev_mode = False

    @classmethod
    def __init__(
            cls,
            level=DEFAULT_LEVEL,
            message_format=DEFAULT_MESSAGE_FORMAT,
            datetime_format=DEFAULT_DATETIME_FORMAT,
            dev_mode=False
    ):
        """Sets up basic Config for Root-Logger. Required to execute at least once before using Root-Logger. \n
        - level: Level of Messages to be printed \n
        - message_format: Format for Messages \n
        - datetime_format: Format for Date / Time \n
        - dev_mode: If True, set Level to 'DEBUG' \n
        """
        cls.dev_mode = dev_mode

        if cls.dev_mode:
            level = 'DEBUG'
            logging.basicConfig(level=level.strip().upper(), format=message_format.strip())
            logging.debug(f'Set basic Config (Dev-mode: {cls.dev_mode}, Level: \'{level}\', '
                          f'Message-format: {message_format}, Datetime-format: {datetime_format}).')
        else:
            logging.basicConfig(level=level.strip().upper(), format=message_format.strip(),
                                datefmt=datetime_format.strip())
            logging.debug(f'Set basic Config (Level: \'{level}\', Message-format: {message_format}, '
                          f'Datetime-format: {datetime_format}).')

    @classmethod
    def create_logger(
            cls, name=DEFAULT_NAME, level=DEFAULT_LEVEL,
            file=DEFAULT_LOG_FILE, remove_old_file=True,
            message_format=DEFAULT_MESSAGE_FORMAT, datetime_format=DEFAULT_DATETIME_FORMAT,
            capitalize_name=True, propagate_to_parent=False, dev_mode=False
    ) -> logging.Logger:
        """Creates & returns a Logger-object. \n
        - name: Name of Logger \n
        - level: Level of Messages to be printed \n
        - file: Path of Log-file. Not writing to Log-file, if value is empty \n
        - remove_old_file: If True, delete old Log-file (if it exists) c
        - message_format: Format for Messages \n
        - datetime_format: Format for Date / Time \n
        - capitalize_log_name: If True, capitalize name \n
        - dev_mode: If True, set Level to 'DEBUG' \n
        """
        logging.debug(f'Creating Logger: Name: {name}, Level: {level}, Log-file: {file}, Dev-mode: {dev_mode}...')

        if capitalize_name:
            name = name.upper()
        if dev_mode:
            level = 'DEBUG'

        # set Name & Level:
        logger = logging.getLogger(name=name.strip())
        logger.setLevel(level='DEBUG')

        # add StreamHandler:
        stream_handler = logging.StreamHandler()
        stream_handler.addFilter(LevelFilter(cls.level_str_to_int(level.strip().upper())))
        stream_handler.setFormatter(logging.Formatter(message_format.strip(), datefmt=datetime_format.strip()))
        logger.addHandler(stream_handler)

        if not propagate_to_parent:
            # propagate Messages to Root-Logger:
            logger.propagate = False

        if remove_old_file and Path(file).is_file():
            os.remove(file)
            logger.debug('...deleted old Log-file...')

        if len(file) >= 1:
            # add FileHandler:
            file_handler = logging.FileHandler(file)
            file_handler.addFilter(LevelFilter(logging.DEBUG))
            file_handler.setFormatter(logging.Formatter(message_format.strip(), datefmt=datetime_format.strip()))
            logger.addHandler(file_handler)

        if dev_mode:
            logger.debug(f'...created Logger (Name: {logger.name}, Level: {logger.level}, Dev-mode: {dev_mode}).')
        else:
            logger.debug(f'...created Logger (Name: {logger.name}, Level: {logger.level}).')
        return logger

    @staticmethod
    def level_str_to_int(level: str) -> int:
        """Takes Level as String and returns it as Integer. If Level is invalid, Method returns Level 'NOTSET' (0). \n
        - level: Level-Sting to get as Integer
        """
        level = level.strip().upper()

        if level == 'DEBUG':
            return 10
        elif level == 'INFO':
            return 20
        if level == 'WARNING':
            return 30
        if level == 'ERROR':
            return 40
        if level == 'CRITICAL':
            return 50
        else:
            return 0
