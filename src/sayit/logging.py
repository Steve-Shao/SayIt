"""SayIt logging configuration."""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path.home() / ".config" / "sayit" / "logs"
LOG_FILE = LOG_DIR / "sayit.log"

# Max 5 log files, 1MB each
MAX_BYTES = 1_000_000
BACKUP_COUNT = 5


def setup_logging(verbose: bool = False) -> logging.Logger:
    """Configure and return the sayit logger.
    
    Args:
        verbose: If True, set DEBUG level; otherwise INFO level.
    
    Returns:
        Configured logger instance.
    """
    logger = logging.getLogger("sayit")
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    level = logging.DEBUG if verbose else logging.INFO
    logger.setLevel(level)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_format = logging.Formatter("%(levelname)s: %(message)s")
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    
    # File handler with rotation
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=MAX_BYTES,
        backupCount=BACKUP_COUNT,
    )
    file_handler.setLevel(logging.DEBUG)  # Always log debug to file
    file_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)
    
    return logger


def get_logger() -> logging.Logger:
    """Get the sayit logger."""
    return logging.getLogger("sayit")
