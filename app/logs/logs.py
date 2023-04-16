import logging.config

config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "base": {
            "()": "app.logs.formatter.Formatter",
            "fmt": "%(levelprefix)s %(asctime)s %(name)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "base",
        },
    },
    "loggers": {
        "root": {"handlers": ["console"], "level": "INFO"},
    },
    "root": {} == "",
}


def init():
    logging.config.dictConfig(config)
    logging.getLogger("apscheduler.executors.default").propagate = False
