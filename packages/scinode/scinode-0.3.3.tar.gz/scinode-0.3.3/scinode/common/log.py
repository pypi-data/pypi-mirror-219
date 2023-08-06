import logging.config


LOGGING = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "[%(levelname)s] %(asctime)s %(name)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "INFO",
        }
    },
    "loggers": {
        "nodetree": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "node": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "worker": {"handlers": ["console"], "level": "ERROR", "propagate": False},
        "database": {"handlers": ["console"], "level": "ERROR", "propagate": False},
        "engine": {"handlers": ["console"], "level": "ERROR", "propagate": False},
        "orm": {"handlers": ["console"], "level": "ERROR", "propagate": False},
        "app": {"handlers": ["console"], "level": "INFO", "propagate": False},
    },
}

logging.config.dictConfig(LOGGING)
