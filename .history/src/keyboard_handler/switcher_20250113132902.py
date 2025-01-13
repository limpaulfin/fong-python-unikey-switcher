"""
Related files:
- src/main.py: File chính của ứng dụng
- src/utils/logger.py: Module logging
- logs/debug.log: File log debug
- logs/error.log: File log lỗi

Chức năng:
- Xử lý sự kiện bàn phím
- Chuyển đổi ngôn ngữ nhập liệu bằng phím Control phải
- Vô hiệu hóa phím Control phải và chuyển thành tổ hợp Control+Shift
"""

import keyboard
from time import sleep
from src.utils.logger import logger

def disable_right_control():
    try:
        keyboard.block_key('right ctrl')
        logger.debug('Đã vô hiệu hóa phím Control phải')
    except Exception as e:
        logger.error(f'Lỗi khi vô hiệu hóa phím Control: {str(e)}')

def switch_language():
    try:
        logger.debug('Bắt đầu chuyển ngôn ngữ')
        keyboard.press('ctrl+shift')
        logger.debug('Đã nhấn Control+Shift')
        sleep(0.3)
        keyboard.release('ctrl+shift')
        logger.debug('Đã thả Control+Shift')
        logger.debug('Đã chuyển ngôn ngữ thành công')
    except Exception as e:
        logger.error(f'Lỗi khi chuyển ngôn ngữ: {str(e)}')

def setup_keyboard_handler():
    try:
        # Vô hiệu hóa phím Control phải
        disable_right_control()

        # Đăng ký hotkey mới
        keyboard.on_press_key('right ctrl', lambda _: switch_language())
        logger.info("Đã đăng ký hotkey thành công")
    except Exception as e:
        logger.error(f'Lỗi khi thiết lập keyboard handler: {str(e)}')
