"""
Related files:
- src/main.py: File chính của ứng dụng
- src/utils/logger.py: Module logging
- logs/debug.log: File log debug
- logs/error.log: File log lỗi
- right-shift-icon.png: Icon mặc định
- right-shift-icon-on.png: Icon khi đang chuyển ngôn ngữ

Chức năng:
- Xử lý sự kiện bàn phím
- Chuyển đổi ngôn ngữ khi nhấn phím Shift phải
- Cho phép nhấn Right Shift nhiều lần để chuyển ngôn ngữ nhiều lần
- Chỉ block input khi đang trong quá trình chuyển ngôn ngữ
- Whitelist cho phép Right Shift, Control, Left Shift hoạt động bình thường
- Hiển thị icon trên taskbar và thay đổi icon theo trạng thái
"""

import keyboard
from time import sleep, time
import pystray
from PIL import Image
import os
from threading import Thread, Lock
from src.utils.logger import logger

# Biến toàn cục để lưu icon và trạng thái
tray_icon = None
is_processing = False  # Flag để kiểm soát quá trình xử lý
switch_count = 0  # Số lần cần chuyển ngôn ngữ
SWITCH_COOLDOWN = 0.1  # Thời gian chờ giữa các lần chuyển
BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
switch_lock = Lock()  # Lock để đồng bộ hóa việc chuyển ngôn ngữ

# Whitelist các phím được phép
WHITELISTED_SCANCODES = {
    54,  # Right Shift
    29,  # Control
    42,  # Left Shift
}

def update_icon(is_active=False):
    """Cập nhật icon dựa trên trạng thái"""
    try:
        if tray_icon:
            icon_name = 'right-shift-icon-on.png' if is_active else 'right-shift-icon.png'
            icon_path = os.path.join(BASE_PATH, icon_name)
            image = Image.open(icon_path)
            tray_icon.icon = image
            logger.debug(f'Đã cập nhật icon sang trạng thái: {"đang chuyển" if is_active else "bình thường"}')
    except Exception as e:
        logger.error(f'Lỗi khi cập nhật icon: {str(e)}')

def switch_language():
    """Thực hiện chuyển ngôn ngữ một lần"""
    try:
        keyboard.press('ctrl')
        keyboard.press('left shift')
        sleep(0.1)
        keyboard.release('left shift')
        keyboard.release('ctrl')
        logger.debug('Đã chuyển ngôn ngữ thành công')
        return True
    except Exception as e:
        logger.error(f'Lỗi khi chuyển ngôn ngữ: {str(e)}')
        return False

def process_language_switches():
    """Xử lý việc chuyển ngôn ngữ nhiều lần"""
    global switch_count, is_processing

    def switch_thread():
        global switch_count, is_processing
        with switch_lock:
            try:
                update_icon(True)
                while switch_count > 0:
                    if switch_language():
                        switch_count -= 1
                        if switch_count > 0:
                            sleep(SWITCH_COOLDOWN)
                    else:
                        break
            finally:
                switch_count = 0
                is_processing = False
                update_icon(False)
                logger.debug('Hoàn tất quá trình chuyển ngôn ngữ')

    Thread(target=switch_thread, daemon=True).start()

def on_any_key(event):
    """Xử lý sự kiện bàn phím"""
    global switch_count, is_processing

    # Log thông tin phím
    logger.debug(f'Phím được nhấn: {event.name}, Scan code: {event.scan_code}, Event: {event.event_type}')

    # Cho phép các phím trong whitelist
    if event.scan_code in WHITELISTED_SCANCODES:
        # Xử lý Right Shift
        if event.scan_code == 54 and event.event_type == 'down':
            switch_count += 1
            logger.debug(f'Đã nhấn Right Shift, số lần cần chuyển: {switch_count}')

            if not is_processing:
                is_processing = True
                process_language_switches()
        return True

    # Block input khi đang xử lý chuyển ngôn ngữ
    if is_processing:
        logger.debug(f'Block phím {event.name} do đang xử lý chuyển ngôn ngữ')
        return False

    return True

def create_tray_icon():
    try:
        global tray_icon
        # Đường dẫn đến file icon mặc định
        icon_path = os.path.join(BASE_PATH, 'right-shift-icon.png')

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
