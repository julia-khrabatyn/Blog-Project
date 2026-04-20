from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def get_logging_config(debug):
    LOG_DIR = BASE_DIR / "logs"
    LOG_DIR.mkdir(exist_ok=True)

    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "{levelname} {asctime} {module} {message}",
                "style": "{",
            },
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
            },
            "file_prod": {
                "level": "ERROR",
                "class": "logging.FileHandler",
                "filename": LOG_DIR / "production_errors.log",
                "formatter": "verbose",
            },
            "file_dev": {
                "level": "DEBUG",
                "class": "logging.FileHandler",
                "filename": LOG_DIR / "dev_debug.log",
                "formatter": "verbose",
            },
        },
        "loggers": {
            "django": {
                "handlers": (
                    ["console", "file_dev"] if debug else ["file_prod"]
                ),
                "level": "DEBUG" if debug else "ERROR",
                "propagate": True,
            },
            "accounts": {
                "handlers": (
                    ["console", "file_dev"] if debug else ["file_prod"]
                ),
                "level": "DEBUG" if debug else "ERROR",
                "propagate": True,
            },
        },
    }
