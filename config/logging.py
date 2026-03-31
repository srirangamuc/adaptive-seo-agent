from __future__ import annotations

import logging
import logging.config
from pathlib import Path

from config.settings import Settings


def setup_logging(settings: Settings) -> None:
    logs_dir = Path("logs")
    logs_dir.mkdir(parents=True, exist_ok=True)

    log_file = logs_dir / "app.log"
    level = settings.log_level.upper()

    log_format = (
        '{"time":"%(asctime)s","level":"%(levelname)s","name":"%(name)s",'
        '"message":"%(message)s"}'
    )

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "json": {"format": log_format},
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "json",
                    "level": level,
                },
                "file": {
                    "class": "logging.FileHandler",
                    "formatter": "json",
                    "level": level,
                    "filename": str(log_file),
                    "encoding": "utf-8",
                },
            },
            "root": {
                "handlers": ["console", "file"],
                "level": level,
            },
        }
    )
