import logging
import os
import sys


# Create logs directory if it doesn't exist
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Paths for log files
ERROR_LOG_FILE = os.path.join(LOG_DIR, "error.log")
INFO_LOG_FILE = os.path.join(LOG_DIR, "info.log")

# Main logger configuration
logger = logging.getLogger("healthcare_logger")
logger.setLevel(logging.DEBUG)  # Log all levels from DEBUG and above

# Formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

# FileHandler: Log WARNING and above to error.log
error_handler = logging.FileHandler(ERROR_LOG_FILE, encoding="utf-8")
error_handler.setLevel(logging.WARNING)  # Log WARNING, ERROR, CRITICAL
error_handler.setFormatter(formatter)

# FileHandler: Log DEBUG and INFO to info.log
info_handler = logging.FileHandler(INFO_LOG_FILE, encoding="utf-8")
info_handler.setLevel(logging.DEBUG)  # Log DEBUG and INFO
info_handler.addFilter(lambda record: record.levelno <= logging.INFO)  # Filter DEBUG and INFO only
info_handler.setFormatter(formatter)

# StreamHandler: Log WARNING and above to console
# console_handler = logging.StreamHandler(sys.stdout)
# console_handler.setLevel(logging.WARNING)  # Log WARNING, ERROR, CRITICAL
# console_handler.setFormatter(formatter)

# Avoid adding handlers multiple times
if not logger.handlers:
    logger.addHandler(error_handler)
    logger.addHandler(info_handler)
    # logger.addHandler(console_handler)
