import logging
from enum import Enum


class Level(Enum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    ERROR = logging.ERROR


class Logger:
    def __init__(self):
        logging.basicConfig(level=logging.INFO,
                            format='\n%(asctime)s - %(levelname)s - %(message)s')

    @staticmethod
    def write(level: Level, *args):
        logging.log(level.value, ' '.join(map(str, args)))


log = Logger()
