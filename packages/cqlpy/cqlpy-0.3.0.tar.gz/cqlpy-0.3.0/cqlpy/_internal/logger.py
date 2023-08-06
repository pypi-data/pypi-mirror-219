from logging import getLogger
import os

APP_NAME = "cqlpy"
LOG_LEVEL_ENV_VAR = "CQLPY_LOG_LEVEL"


def get_logger():
    logger = getLogger(APP_NAME)
    if (level := os.environ.get(LOG_LEVEL_ENV_VAR)) is not None:
        logger.setLevel(level)

    return logger
