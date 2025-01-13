# Python Unikey Switcher

Ứng dụng chuyển đổi ngôn ngữ nhập liệu bằng phím Windows phải.

## Tính năng

-   Chuyển đổi ngôn ngữ nhập liệu bằng phím Windows phải
-   Vô hiệu hóa chức năng mặc định của phím Windows phải
-   Ghi log để debug

## Cài đặt

1. Clone repository:
 <pre>
 git clone https://github.com/yourusername/python-unikey-switcher.git
 cd python-unikey-switcher
 </pre>

2. Cài đặt dependencies:
 <pre>
 pip install -r requirements.txt
 </pre>

## Sử dụng

Chạy file main.py:

<pre>
python src/main.py
</pre>

## Cấu trúc thư mục

<pre>
python-unikey-switcher/
├── src/
│   ├── __init__.py
│   ├── main.py           # File chính
│   ├── keyboard_handler/ # Module xử lý keyboard
│   │   ├── __init__.py
│   │   └── switcher.py   # Logic chuyển ngôn ngữ
│   └── utils/           # Các tiện ích
│       ├── __init__.py
│       └── logger.py    # Module logging
├── logs/
│   ├── debug.log
│   └── error.log
├── tests/              # Thư mục chứa tests
│   └── __init__.py
├── README.md          # Hướng dẫn sử dụng
├── requirements.txt   # Dependencies
└── setup.py          # Cấu hình package
</pre>

## Yêu cầu hệ thống

-   Python 3.6+
-   Windows 10/11

## License

MIT License
