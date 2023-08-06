import logging
from rich.logging import RichHandler

#LOG_FORMAT = '%(asctime)s -- %(levelname)s: %(message)s'
LOG_FORMAT = '%(message)s'

logging.basicConfig(format=LOG_FORMAT, datefmt="[%X]", handlers=[RichHandler(rich_tracebacks=True)])

def get_logger(name: str=None, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger

default_logger = get_logger()