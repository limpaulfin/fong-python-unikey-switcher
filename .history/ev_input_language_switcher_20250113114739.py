"""
Related files:
- .cursorrules: Quy tắc coding
- context.md: Yêu cầu và tài liệu
- config.json: File cấu hình (optional)
- debug.log: File log debug
- error.log: File log lỗi

Chức năng:
- Bắt và xử lý sự kiện phím
- Chuyển đổi ngôn ngữ khi nhấn Windows phải
- Vô hiệu hóa chức năng mặc định của Windows phải
- Ghi log debug và lỗi
"""

import keyboard
import win32api
import win32con
from time import sleep
import logging
import logging.handlers
import os
from datetime import datetime

# Thiết lập logging
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

def disable_right_windows():
    try:
        keyboard.block_key('right windows')
        logger.debug('Đã vô hiệu hóa phím Windows phải')
    except Exception as e:
        logger.error(f'Lỗi khi vô hiệu hóa phím Windows: {str(e)}')

def switch_language():
    try:
        # Ghi log trước khi chuyển
        logger.debug('Bắt đầu chuyển ngôn ngữ')

        # Giả lập tổ hợp phím Ctrl+Shift
        keyboard.press('ctrl+shift')
        sleep(0.1)
        keyboard.release('ctrl+shift')

        logger.debug('Đã chuyển ngôn ngữ thành công')
    except Exception as e:
        logger.error(f'Lỗi khi chuyển ngôn ngữ: {str(e)}')

def main():
    try:
        logger.info("Khởi động chương trình...")

        # Vô hiệu hóa phím Windows phải
        disable_right_windows()

        # Đăng ký hotkey mới
        keyboard.on_press_key('right windows', lambda _: switch_language())
        logger.info("Đã đăng ký hotkey thành công")

        # Giữ chương trình chạy
        keyboard.wait()
    except Exception as e:
        logger.error(f'Lỗi trong hàm main: {str(e)}')

if __name__ == "__main__":
    # Khởi tạo logger
    logger = setup_logging()
    main()
