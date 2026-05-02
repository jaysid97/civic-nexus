"""
Configuration module for the Election Process Education application.
Handles loading environment variables and basic configuration.
"""

import os
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration variables."""
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def validate(cls) -> None:
        """Validate critical configuration variables."""
        if not cls.GEMINI_API_KEY or cls.GEMINI_API_KEY == "your_gemini_api_key_here":
            logging.warning("GEMINI_API_KEY is missing or invalid. App will not function properly.")

Config.validate()
