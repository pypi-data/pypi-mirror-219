import logging
import sys

import loguru


class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = sys._getframe(6), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(InterceptHandler())


def configure_logger():
    loguru.logger.configure(
        handlers=[
            {
                "sink": "output.log",
                "enqueue": True,
                "backtrace": True,
                "diagnose": True,
                "rotation": "8 MB",
                "level": "INFO",
                "format": "<green>{time:YYYY-DD-MM HH:mm:ss}</green> - <level>{level}</level> - <cyan>{name}</cyan>: <level>{message}</level>",
            },
            {
                "sink": sys.stdout,
                "colorize": True,
                "backtrace": True,
                "diagnose": True,
                "level": "INFO",
                "format": "<green>{time:YYYY-DD-MM HH:mm:ss}</green> - <level>{level}</level> - <cyan>{name}</cyan>: <level>{message}</level>",
            },
        ]
    )
    return loguru.logger


logger = configure_logger()
log = logger
