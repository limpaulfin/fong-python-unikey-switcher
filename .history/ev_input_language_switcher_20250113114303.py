"""
Related files:
- .cursorrules: Quy tắc coding
- context.md: Yêu cầu và tài liệu
- config.json: File cấu hình (optional)

Chức năng:
- Bắt và xử lý sự kiện phím
- Chuyển đổi ngôn ngữ khi nhấn Windows phải
- Vô hiệu hóa chức năng mặc định của Windows phải
"""

import keyboard
import win32api
import win32con
from time import sleep

def disable_right_windows():
    keyboard.block_key('right windows')

def switch_language():
    # Giả lập tổ hợp phím Ctrl+Shift
    keyboard.press('ctrl+shift')
    sleep(0.1)
    keyboard.release('ctrl+shift')

def main():
    print("Starting keyboard mapper...")

    # Vô hiệu hóa phím Windows phải
    disable_right_windows()

    # Đăng ký hotkey mới
    keyboard.on_press_key('right windows', lambda _: switch_language())

    # Giữ chương trình chạy
    keyboard.wait()

if __name__ == "__main__":
    main()
