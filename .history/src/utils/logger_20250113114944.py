"""
Related files:
- src/main.py: File chính của ứng dụng
- logs/debug.log: File log debug
- logs/error.log: File log lỗi

Chức năng:
- Khởi tạo và cấu hình logging
- Cung cấp logger cho toàn bộ ứng dụng
"""

import logging
import logging.handlers
import os
from datetime import datetime

def setup_logging():
    # Tạo thư mục logs nếu chưa tồn tại
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Thiết lập logger chính
    logger = logging.getLogger('EVKeyboardSwitcher')
    logger.setLevel(logging.DEBUG)

    # Format log
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Debug log file
    debug_handler = logging.handlers.RotatingFileHandler(
        'logs/debug.log',
        maxBytes=1024*1024,  # 1MB
        backupCount=5
    )
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(formatter)

    # Error log file
    error_handler = logging.handlers.RotatingFileHandler(
        'logs/error.log',
        maxBytes=1024*1024,  # 1MB
        backupCount=5
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Thêm handlers vào logger
    logger.addHandler(debug_handler)
    logger.addHandler(error_handler)
    logger.addHandler(console_handler)

    return logger

# Tạo và export logger instance
logger = setup_logging()
