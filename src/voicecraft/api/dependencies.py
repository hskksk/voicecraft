"""
Dependency injection for FastAPI
"""

import logging
from typing import Generator
from fastapi import Depends

def get_logger() -> logging.Logger:
    """Get logger instance"""
    return logging.getLogger("voicecraft.api")

# Placeholder for future dependencies
# def get_speech_synthesizer():
#     """Get speech synthesizer instance"""
#     pass

# def get_config_manager():
#     """Get configuration manager"""
#     pass
