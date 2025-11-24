# logger.py
import logging
from logging.handlers import RotatingFileHandler
import sys

# Create a logger
logger = logging.getLogger("crud_api")  # give your app a name
logger.setLevel(logging.INFO)  # default level

# Console handler (prints to stdout)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

# File handler with rotation (max 5 MB per file, keep 3 backups)
file_handler = RotatingFileHandler("app.log", maxBytes=5*1024*1024, backupCount=3)
file_handler.setLevel(logging.INFO)

# Log format
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s"
)
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
