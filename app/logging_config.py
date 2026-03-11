import logging
import logging.config
import sys

from app.config import settings

LOGGING_CONFIG: dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "format": (
                '{"time": "%(asctime)s", "level": "%(levelname)s", '
                '"name": "%(name)s", "message": "%(message)s"}'
            ),
            "datefmt": "%Y-%m-%dT%H:%M:%S",
        },
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S",
        },
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "json",
        },
    },
    "root": {
        "level": settings.log_level.upper(),
        "handlers": ["stdout"],
    },
    "loggers": {
        "uvicorn": {"propagate": True},
        "fastapi": {"propagate": True},
    },
}


def setup_logging() -> None:
    logging.config.dictConfig(LOGGING_CONFIG)
