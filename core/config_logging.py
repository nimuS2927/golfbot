import logging
import logging.config
from logging.handlers import TimedRotatingFileHandler
from pythonjsonlogger import jsonlogger
from core.config import c_basic
from pathlib import Path

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "format": "%(asctime)s [%(levelname)s]  %(name)s: %(message)s [%(module)s]",
            "datefmt": "%Y-%m-%dT%H:%M:%SZ",
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
        }
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "stream": "ext://sys.stdout",
            "formatter": "json",
        },
        "logfile": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "INFO",
            "filename": f"{Path.joinpath(c_basic.path_to_logging, 'log_file.log')}",
            "formatter": "json",
            "when": "M",
            "interval": 1,
            "backupCount": 3,
            "delay": True,
            "utc": True,
        }
    },
    "loggers": {
        "": {
            "handlers": ["stdout", "logfile"],
            "level": "DEBUG"
        }
    },
}
