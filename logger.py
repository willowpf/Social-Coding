import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime

def setup_logger(name):
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Create a custom logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Create handlers
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    file_handler = RotatingFileHandler(
        f'logs/navigation_{datetime.now().strftime("%Y%m%d")}.log',
        maxBytes=1024000,
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    
    # Create formatters and add it to handlers
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    console_format = '%(levelname)s - %(message)s'
    
    file_handler.setFormatter(logging.Formatter(log_format))
    console_handler.setFormatter(logging.Formatter(console_format))
    
    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger