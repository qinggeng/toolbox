import os
import re

# 搜索文件
def search_files(*, start_dir, file_name, skip_dirs):
    """
    搜索文件

    :param start_dir: 搜索的起始目录
    :param file_name: 要搜索的文件名
    :param skip_dirs: 要跳过的目录
    :return: 返回一个字典，键为目录，值为文件路径，如果没有找到文件则值为 None
    """
    result = {}
    for root, dirs, files in os.walk(start_dir):
        for skip_dir in skip_dirs:
            if re.search(skip_dir, root):
                break
        else:
            found_file = False
            for file in files:
                if file == file_name:
                    result[root] = os.path.join(root, file)
                    found_file = True
                    break
            if not found_file:
                result[root] = None
    return result
