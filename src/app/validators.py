from .config import settings
from .logger import logger


def validate_settings():
    """Validate required settings"""
    required_settings = ["app_name", "version", "host", "port"]
    
    missing = []
    for setting in required_settings:
        if not hasattr(settings, setting):
            missing.append(setting)
    
    if missing:
        error_msg = f"Missing required settings: {', '.join(missing)}"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    logger.info("All required settings validated successfully")