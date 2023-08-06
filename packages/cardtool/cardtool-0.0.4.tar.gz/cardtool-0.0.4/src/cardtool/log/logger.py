import sys

from loguru import logger


def configure_logger():
    logger.remove()
    configuration = {
        "handlers": [
            {
                "sink": sys.stdout,
                "colorize": True,
                "format": "<level>[{level}]</level> <fg #ffffff>{time:YYYY-MM-DD HH:mm:ss}</fg #ffffff>: <lvl>{message}</lvl>",  # noqa: E501
            }
        ],
        "levels": [
            {"name": "INFO", "color": "<blue>"},
            {"name": "WARNING", "color": "<fg #ffa500>"},
        ],
    }
    logger.configure(**configuration)
