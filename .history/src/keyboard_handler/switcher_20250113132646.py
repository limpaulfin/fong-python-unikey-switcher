"""
Related files:
- src/main.py: File chính của ứng dụng
- src/utils/logger.py: Module logging
- logs/debug.log: File log debug
- logs/error.log: File log lỗi

Chức năng:
- Xử lý sự kiện bàn phím
- Chuyển đổi ngôn ngữ nhập liệu
- Vô hiệu hóa phím Windows phải
"""

import keyboard
from time import sleep
from src.utils.logger import logger

def disable_right_windows():
    try:
        keyboard.block_key('right windows')
        logger.debug('Đã vô hiệu hóa phím Windows phải')
    except Exception as e:
        logger.error(f'Lỗi khi vô hiệu hóa phím Windows: {str(e)}')

def switch_language():
    try:
        logger.debug('Bắt đầu chuyển ngôn ngữ')
        keyboard.press('alt+shift')
        logger.debug('Đã nhấn Alt+Shift')
        sleep(0.3)
        keyboard.release('alt+shift')
        logger.debug('Đã thả Alt+Shift')
        logger.debug('Đã chuyển ngôn ngữ thành công')
    except Exception as e:
        logger.error(f'Lỗi khi chuyển ngôn ngữ: {str(e)}')

def setup_keyboard_handler():
    try:
        # Vô hiệu hóa phím Windows phải
        disable_right_windows()

        # Đăng ký hotkey mới
        keyboard.on_press_key('right windows', lambda _: switch_language())
        logger.info("Đã đăng ký hotkey thành công")
    except Exception as e:
        logger.error(f'Lỗi khi thiết lập keyboard handler: {str(e)}')
