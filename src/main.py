"""
Related files:
- src/keyboard_handler/switcher.py: Module xử lý keyboard
- src/utils/logger.py: Module logging
- src/utils/tree_generator.py: Module tạo cây thư mục
- src/utils/dependency_checker.py: Module kiểm tra dependencies
- logs/debug.log: File log debug
- logs/error.log: File log lỗi
- .env: File cấu hình
- .files-dir-tree.md: File cấu trúc thư mục

Chức năng:
- Điểm vào chính của ứng dụng
- Khởi tạo các module
- Duy trì vòng lặp chính
- Sử dụng pynput để bắt sự kiện bàn phím (không cần quyền admin)
"""

import os
import sys
import threading
import time

# Thêm thư mục gốc vào PYTHONPATH
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Kiểm tra và cài đặt dependencies
from src.utils.dependency_checker import check_and_install_dependencies, setup_python_path
setup_python_path()
check_and_install_dependencies()

# Import các module khác
try:
    from pynput import keyboard
    from src.utils.logger import logger
    from src.keyboard_handler.switcher import setup_keyboard_handler
    from src.utils.tree_generator import update_tree_file
except ImportError as e:
    print(f"Lỗi import module: {str(e)}")
    print("Vui lòng kiểm tra lại cài đặt và thử lại")
    sys.exit(1)

def main():
    try:
        logger.info("Khởi động chương trình...")

        # Cập nhật file cấu trúc thư mục nếu DEBUG=True
        update_tree_file()

        # Thiết lập keyboard handler
        keyboard_handler = setup_keyboard_handler()

        # Tạo và khởi động keyboard listener
        with keyboard.Listener(
            on_press=keyboard_handler.on_press,
            on_release=keyboard_handler.on_release
        ) as listener:
            listener.join()  # Giữ chương trình chạy

    except Exception as e:
        logger.error(f'Lỗi trong hàm main: {str(e)}')

if __name__ == "__main__":
    main()
