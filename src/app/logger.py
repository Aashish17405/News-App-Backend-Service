import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from .config import settings


def setup_logger(name: str = "app") -> logging.Logger:
    """
    Setup application logger with console and file handlers.
    
    Args:
        name: Logger name (default: "app")
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Set log level based on environment
    log_level = logging.DEBUG if settings.debug else logging.INFO
    logger.setLevel(log_level)
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Console handler (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    
    # File handler (rotating)
    file_handler = RotatingFileHandler(
        log_dir / "app.log",
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
    )
    file_handler.setLevel(log_level)
    
    # Error file handler (only errors)
    error_file_handler = RotatingFileHandler(
        log_dir / "error.log",
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
    )
    error_file_handler.setLevel(logging.ERROR)
    
    # Formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    
    # Detailed formatter for file logs
    detailed_formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    
    # Set formatters
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(detailed_formatter)
    error_file_handler.setFormatter(detailed_formatter)
    
    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(error_file_handler)
    
    return logger


# Create default logger instance
logger = setup_logger()