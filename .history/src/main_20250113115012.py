"""
Related files:
- src/keyboard_handler/switcher.py: Module xử lý keyboard
- src/utils/logger.py: Module logging
- logs/debug.log: File log debug
- logs/error.log: File log lỗi

Chức năng:
- Điểm vào chính của ứng dụng
- Khởi tạo các module
- Duy trì vòng lặp chính
"""

import keyboard
from src.utils.logger import logger
from src.keyboard_handler.switcher import setup_keyboard_handler

def main():
    try:
        logger.info("Khởi động chương trình...")

        # Thiết lập keyboard handler
        setup_keyboard_handler()

        # Giữ chương trình chạy
        keyboard.wait()
    except Exception as e:
        logger.error(f'Lỗi trong hàm main: {str(e)}')

if __name__ == "__main__":
    main()
