import os
import sys

import loguru


def create_logger(level="INFO"):
    log_level = os.getenv("LOGLEVEL", level)
    root_logger = loguru.logger

    try:
        root_logger.remove()
        root_logger.add(sys.stderr, level=log_level)
    except Exception as e:
        root_logger.add(sys.stderr, level="DEBUG")
        return root_logger

    return root_logger


logger = create_logger()
