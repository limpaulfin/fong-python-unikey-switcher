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

def generate_tree(start_path='.'):
    """Tạo cây thư mục dạng markdown."""
    tree = []

    for root, dirs, files in os.walk(start_path):
        # Bỏ qua thư mục .git và các file/thư mục ẩn
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        files = [f for f in files if not f.startswith('.')]

        level = root.replace(start_path, '').count(os.sep)
        indent = '│   ' * level

        if level > 0:
            tree.append(f'{indent[:-4]}├── {os.path.basename(root)}/')

        for file in files:
            tree.append(f'{indent}├── {file}')

    return '\n'.join(tree)

def update_tree_file():
    """Cập nhật file cấu trúc thư mục nếu DEBUG=True."""
    # Load biến môi trường
    load_dotenv()

    # Kiểm tra DEBUG mode
    if os.getenv('DEBUG', 'False').lower() != 'true':
        return

    # Lấy đường dẫn file tree
    tree_file = os.getenv('TREE_FILE', '.files-dir-tree.md')

    # Tạo cây thư mục
    tree_content = f"""# Cấu trúc thư mục dự án
<pre>
{generate_tree()}
</pre>
"""

    # Ghi vào file
    with open(tree_file, 'w', encoding='utf-8') as f:
        f.write(tree_content)
