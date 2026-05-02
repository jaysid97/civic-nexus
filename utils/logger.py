"""
Logger utility module.
Provides a centralized logging configuration for the application.
"""

import logging
from config import Config

def setup_logger(name: str) -> logging.Logger:
    """
    Sets up and returns a configured logger.
    
    Args:
        name (str): The name of the logger (usually __name__).
        
    Returns:
        logging.Logger: The configured logger instance.
    """
    logger = logging.getLogger(name)
    
    # Only configure if it doesn't already have handlers to avoid duplication
    if not logger.handlers:
        logger.setLevel(getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO))
        
        # Create console handler
        ch = logging.StreamHandler()
        ch.setLevel(getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO))
        
        # Create formatter and add it to the handler
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        
        # Add handler to the logger
        logger.addHandler(ch)
        
    return logger
