"""
Related files:
- src/main.py: File chính của ứng dụng
- src/utils/logger.py: Module logging
- logs/debug.log: File log debug
- logs/error.log: File log lỗi
- right-shift-icon.png: Icon hiển thị trên taskbar

Chức năng:
- Xử lý sự kiện bàn phím
- Chuyển đổi ngôn ngữ nhập liệu khi nhấn phím Shift phải
- Khi nhấn Right Shift sẽ kích hoạt tổ hợp Control + Left Shift
- Hiển thị icon trên taskbar
"""

import keyboard
from time import sleep
import pystray
from PIL import Image
import os
from src.utils.logger import logger

# Biến toàn cục để lưu icon
tray_icon = None

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

def create_tray_icon():
    try:
        global tray_icon
        # Đường dẫn đến file icon
        icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'right-shift-icon.png')

        # Tạo menu cho icon
        def on_exit(icon, item):
            icon.stop()
            os._exit(0)

        # Tạo icon từ file ảnh
        image = Image.open(icon_path)
        menu = pystray.Menu(
            pystray.MenuItem("Thoát", on_exit)
        )

        # Tạo icon
        tray_icon = pystray.Icon(
            "RightShiftSwitcher",
            image,
            "Right Shift Language Switcher",
            menu
        )

        logger.info("Đã tạo system tray icon thành công")
        return tray_icon
    except Exception as e:
        logger.error(f'Lỗi khi tạo system tray icon: {str(e)}')
        return None

def setup_keyboard_handler():
    try:
        # Thêm hook để bắt sự kiện phím Right Shift
        keyboard.hook(on_any_key)
        logger.info("Đã thiết lập keyboard handler thành công")

        # Tạo và hiển thị system tray icon
        icon = create_tray_icon()
        if icon:
            icon.run()
    except Exception as e:
        logger.error(f'Lỗi khi thiết lập keyboard handler: {str(e)}')
