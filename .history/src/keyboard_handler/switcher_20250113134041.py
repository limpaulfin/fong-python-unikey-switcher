"""
Related files:
- src/main.py: File chính của ứng dụng
- src/utils/logger.py: Module logging
- logs/debug.log: File log debug
- logs/error.log: File log lỗi

Chức năng:
- Xử lý sự kiện bàn phím
- Chuyển đổi ngôn ngữ nhập liệu khi nhấn phím Shift phải
- Khi nhấn Right Shift sẽ kích hoạt tổ hợp Control + Left Shift
"""

import keyboard
from time import sleep
from src.utils.logger import logger

def on_any_key(event):
    logger.debug(f'Phím được nhấn: {event.name}, Scan code: {event.scan_code}')
    # Kiểm tra nếu là phím Right Shift (scan code 54)
    if event.scan_code == 54 and event.event_type == 'down':
        logger.debug('Đã phát hiện phím Right Shift được nhấn')
        switch_language()

def switch_language():
    try:
        logger.debug('Bắt đầu chuyển ngôn ngữ')
        # Sử dụng Control + Left Shift thay vì Control + Shift
        keyboard.press('ctrl')
        keyboard.press('left shift')
        logger.debug('Đã nhấn Control + Left Shift')
        sleep(0.3)
        keyboard.release('left shift')
        keyboard.release('ctrl')
        logger.debug('Đã thả Control + Left Shift')
        logger.debug('Đã chuyển ngôn ngữ thành công')
    except Exception as e:
        logger.error(f'Lỗi khi chuyển ngôn ngữ: {str(e)}')

def setup_keyboard_handler():
    try:
        # Thêm hook để bắt sự kiện phím Right Shift
        keyboard.hook(on_any_key)
        logger.info("Đã thiết lập keyboard handler thành công")
    except Exception as e:
        logger.error(f'Lỗi khi thiết lập keyboard handler: {str(e)}')
