import logging
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Filter gán request_id mặc định
class RequestIDFilter(logging.Filter):
    def filter(self, record):
        if not hasattr(record, "request_id"):
            record.request_id = "N/A"
        return True

# Formatter chuẩn
formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] [%(name)s:%(lineno)d] [req_id=%(request_id)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
console_handler.addFilter(RequestIDFilter())

# File handler
file_handler = RotatingFileHandler(
    os.path.join(LOG_DIR, "chatbot.log"),
    maxBytes=5 * 1024 * 1024,
    backupCount=5,
    encoding="utf-8"
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
file_handler.addFilter(RequestIDFilter())

# Logger chính
logger = logging.getLogger("chatbot")
logger.setLevel(logging.DEBUG)
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# SQLAlchemy logger
sqlalchemy_logger = logging.getLogger("sqlalchemy.engine")
sqlalchemy_logger.setLevel(logging.INFO)
sqlalchemy_logger.addHandler(console_handler)
sqlalchemy_logger.addHandler(file_handler)
sqlalchemy_logger.propagate = False  # quan trọng để tránh log 2 lần
sqlalchemy_logger.addFilter(RequestIDFilter())
