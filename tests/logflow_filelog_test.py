import logging
from pathlib import Path

from sqlalchemy.orm.path_registry import log

# Directories
BASE_DIR = Path(__file__).parent.parent
LOG_FILE = BASE_DIR / "logs" / "app.log"

# Logging configuration
LOG_LEVEL = logging.DEBUG
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def setup_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        level=LOG_LEVEL,
        format=LOG_FORMAT,
        handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()],
    )


def main():
    """Run the application."""
    setup_logging()  # Configure logging

    logger = logging.getLogger(__name__)

    logcount = 20000
    for i in range(logcount):
        logger.info(f"New Processing info {i + 1}/{logcount}")
        logger.warning(f"New Processing warning {i + 1}/{logcount}")
        logger.error(f"New Processing error {i + 1}/{logcount}")
        logger.critical(f"New Processing critical {i + 1}/{logcount}")
        logger.debug(f"New Processing debug {i + 1}/{logcount}")


if __name__ == "__main__":
    main()
