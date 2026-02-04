#!/usr/bin/env python3
"""
Logging configuration module
Provides structured logging for production environments
"""

import logging
import logging.handlers
import os
import sys
from datetime import datetime

def setup_logging(app=None, level=None):
    """
    Configure structured logging for the application
    
    Args:
        app: Flask application instance (optional)
        level: Logging level (default: INFO)
    """
    
    # Determine log level
    if level is None:
        level = os.getenv("LOG_LEVEL", "INFO").upper()
    
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(level)
    
    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # ===========================
    # Console Handler (stdout)
    # ===========================
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    
    # Professional format
    if os.getenv("ENVIRONMENT") == "production":
        # JSON-like format for production (easy to parse)
        console_format = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)-8s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    else:
        # More verbose format for development
        console_format = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)-8s | %(funcName)s:%(lineno)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    
    # ===========================
    # File Handler (optional)
    # ===========================
    log_dir = os.getenv("LOG_DIR", "/tmp")
    if os.path.exists(log_dir) or log_dir == "/tmp":
        try:
            log_file = os.path.join(log_dir, f"pipeline-api-{datetime.now().strftime('%Y%m%d')}.log")
            file_handler = logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=10485760,  # 10MB
                backupCount=5
            )
            file_handler.setLevel(level)
            file_format = logging.Formatter(
                '%(asctime)s | %(name)s | %(levelname)-8s | %(funcName)s:%(lineno)d | %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_format)
            logger.addHandler(file_handler)
        except Exception as e:
            logger.warning(f"Could not set up file logging: {e}")
    
    # ===========================
    # Flask-specific logging
    # ===========================
    if app:
        # Reduce Flask's verbose logging
        logging.getLogger('werkzeug').setLevel(logging.WARNING)
        logging.getLogger('flask').setLevel(logging.WARNING)
        
        # Your app logging
        app_logger = logging.getLogger('main')
        app_logger.setLevel(level)
    
    return logger


def get_logger(name):
    """Get a logger instance"""
    return logging.getLogger(name)


# Suppress noisy loggers
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('gunicorn.access').setLevel(logging.INFO)
