"""
Related files:
- .env: File cấu hình
- .files-dir-tree.md: File chứa cấu trúc thư mục

Chức năng:
- Tạo và cập nhật file cấu trúc thư mục
- Chỉ chạy khi DEBUG=True trong .env
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from src.utils.logger import logger

def get_root_dir():
    """Lấy đường dẫn thư mục gốc của dự án."""
    current_file = os.path.abspath(__file__)
    return os.path.dirname(os.path.dirname(os.path.dirname(current_file)))

def generate_tree(start_path='.'):
    """Tạo cây thư mục dạng markdown."""
    tree = []

    # Chuyển đường dẫn tương đối thành tuyệt đối
    abs_start_path = os.path.abspath(start_path)

    for root, dirs, files in os.walk(abs_start_path):
        # Bỏ qua thư mục .git và các file/thư mục ẩn
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        files = [f for f in files if not f.startswith('.')]

        # Tạo đường dẫn tương đối so với thư mục bắt đầu
        rel_path = os.path.relpath(root, abs_start_path)
        level = 0 if rel_path == '.' else rel_path.count(os.sep) + 1

        indent = '│   ' * level

        if level > 0:
            tree.append(f'{indent[:-4]}├── {os.path.basename(root)}/')

        for file in files:
            tree.append(f'{indent}├── {file}')

    return '\n'.join(tree)

def update_tree_file():
    """Cập nhật file cấu trúc thư mục nếu DEBUG=True."""
    try:
        # Load biến môi trường và chuyển về thư mục gốc
        load_dotenv()
        root_dir = get_root_dir()
        os.chdir(root_dir)

        # Kiểm tra DEBUG mode
        if os.getenv('DEBUG', 'False').lower() != 'true':
            logger.debug('DEBUG=False, bỏ qua tạo cây thư mục')
            return

        # Lấy đường dẫn file tree
        tree_file = os.getenv('TREE_FILE', '.files-dir-tree.md')

        # Tạo cây thư mục từ thư mục gốc
        tree_content = f"""# Cấu trúc thư mục dự án
<pre>
{generate_tree('.')}
</pre>
"""

        # Ghi vào file
        with open(tree_file, 'w', encoding='utf-8') as f:
            f.write(tree_content)

        logger.debug(f'Đã cập nhật file cấu trúc thư mục: {os.path.abspath(tree_file)}')
    except Exception as e:
        logger.error(f'Lỗi khi tạo cây thư mục: {str(e)}')
