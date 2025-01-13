"""
Related files:
- src/main.py: File chính của ứng dụng
- src/utils/logger.py: Module logging
- logs/debug.log: File log debug
- logs/error.log: File log lỗi

Chức năng:
- Xử lý sự kiện bàn phím
- Chuyển đổi ngôn ngữ nhập liệu bằng phím Shift phải
- Vô hiệu hóa phím Shift phải và chuyển thành tổ hợp Control+Shift
"""

import keyboard
from time import sleep
from src.utils.logger import logger

def on_any_key(event):
    logger.debug(f'Phím được nhấn: {event.name}, Scan code: {event.scan_code}')
    # Kiểm tra nếu là phím Right Shift (scan code 54)
    if event.scan_code == 54:
        logger.debug('Đã phát hiện phím Right Shift')
        switch_language()

def disable_right_shift():
    try:
        keyboard.block_key('right shift')
        logger.debug('Đã vô hiệu hóa phím Shift phải')
    except Exception as e:
        logger.error(f'Lỗi khi vô hiệu hóa phím Shift: {str(e)}')

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
        # Thêm hook để bắt tất cả các phím và xử lý Right Shift
        keyboard.hook(on_any_key)

        # Vô hiệu hóa phím Shift phải
        disable_right_shift()

        logger.info("Đã thiết lập keyboard handler thành công")
    except Exception as e:
        logger.error(f'Lỗi khi thiết lập keyboard handler: {str(e)}')
