import logging
from logging.handlers import RotatingFileHandler
import os


BACKUP_COUNT = 3
MAX_BYTES = 10240
LOG_DIRECTORY = f'{os.getcwd()}/logs'


def create_logger(name: str, file_level=logging.DEBUG, console_level=logging.ERROR) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not os.path.exists(LOG_DIRECTORY):
        os.makedirs(LOG_DIRECTORY)

    file_handler = RotatingFileHandler(os.path.join(LOG_DIRECTORY, f'{name}.log'), maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)
    file_handler.setLevel(file_level)
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger