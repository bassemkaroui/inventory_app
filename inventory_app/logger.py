import logging
from logging.handlers import RotatingFileHandler
from math import log
from pathlib import Path


BACKUP_COUNT = 3
MAX_BYTES = 10240
log_path = Path('logs')


def create_logger(name: str, file_level=logging.DEBUG, console_level=logging.ERROR) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not log_path.exists():
        log_path.mkdir()

    file_handler = RotatingFileHandler(log_path/f'{name}.log', maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)
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