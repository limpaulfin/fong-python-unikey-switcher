"""
Related files:
- .env: File cấu hình
- logs/debug.log: File log debug
- logs/error.log: File log lỗi

Chức năng:
- Khởi tạo và cấu hình logging
- Điều chỉnh log level dựa vào DEBUG trong .env
- Ghi log ra file và console
"""

import logging
import logging.handlers
import os
from datetime import datetime
from dotenv import load_dotenv

def setup_logging():
    # Load biến môi trường
    load_dotenv()
    debug_mode = os.getenv('DEBUG', 'False').lower() == 'true'

    # Tạo thư mục logs nếu chưa tồn tại
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Thiết lập logger chính
    logger = logging.getLogger('EVKeyboardSwitcher')
    logger.setLevel(logging.DEBUG if debug_mode else logging.INFO)

    # Format log
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Debug log file - luôn ghi mọi log level
    debug_handler = logging.handlers.RotatingFileHandler(
        'logs/debug.log',
        maxBytes=1024*1024,  # 1MB
        backupCount=5
    )
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(formatter)

    # Error log file - chỉ ghi error
    error_handler = logging.handlers.RotatingFileHandler(
        'logs/error.log',
        maxBytes=1024*1024,  # 1MB
        backupCount=5
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    # Console handler - level phụ thuộc vào DEBUG mode
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if debug_mode else logging.INFO)
    console_handler.setFormatter(formatter)

    # Xóa handlers cũ (nếu có)
    logger.handlers.clear()

    # Thêm handlers vào logger
    logger.addHandler(debug_handler)
    logger.addHandler(error_handler)
    logger.addHandler(console_handler)

    # Log thông tin khởi động
    logger.debug('Logger được khởi tạo ở chế độ DEBUG') if debug_mode else logger.info('Logger được khởi tạo')

    return logger

# Tạo và export logger instance
logger = setup_logging()
