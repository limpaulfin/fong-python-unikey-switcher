"""
Related files:
- requirements.txt: Danh sách dependencies
- .env: File cấu hình

Chức năng:
- Kiểm tra các module cần thiết
- Tự động cài đặt module thiếu nếu DEBUG=True
"""

import os
import sys
import subprocess
from importlib import util
from dotenv import load_dotenv

def is_package_installed(package_name):
    """Kiểm tra package đã được cài đặt chưa."""
    try:
        spec = util.find_spec(package_name)
        return spec is not None
    except ModuleNotFoundError:
        return False

def install_package(package_name):
    """Cài đặt package bằng pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        return True
    except subprocess.CalledProcessError:
        return False

def check_and_install_dependencies():
    """Kiểm tra và cài đặt các dependencies."""
    # Load biến môi trường
    try:
        load_dotenv()
    except:
        # Nếu dotenv chưa được cài đặt, cài đặt nó trước
        if not is_package_installed('dotenv'):
            install_package('python-dotenv')
            load_dotenv()

    # Chỉ cài đặt tự động nếu DEBUG=True
    if os.getenv('DEBUG', 'False').lower() != 'true':
        return

    # Đọc requirements.txt
    try:
        with open('requirements.txt', 'r') as f:
            requirements = [line.strip().split('==')[0] for line in f if line.strip()]
    except FileNotFoundError:
        requirements = ['keyboard', 'pywin32', 'python-dotenv']

    # Kiểm tra và cài đặt từng package
    for package in requirements:
        if not is_package_installed(package):
            print(f"Đang cài đặt {package}...")
            if install_package(package):
                print(f"Đã cài đặt {package} thành công")
            else:
                print(f"Không thể cài đặt {package}")

def setup_python_path():
    """Thêm thư mục gốc vào PYTHONPATH."""
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if root_dir not in sys.path:
        sys.path.append(root_dir)
