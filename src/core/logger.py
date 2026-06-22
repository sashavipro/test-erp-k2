"""src/core/logger.py."""

import logging

from src.core.config import settings


def setup_logging():
    """Set up application logging."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    return logging.getLogger(settings.PROJECT_NAME)


logger = setup_logging()
