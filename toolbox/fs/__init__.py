import os
import re
import fnmatch

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

def find_matching_files(directory_list, filename_templates):
    """查找给定目录下所有匹配指定文件名模板的文件

    参数:
    directory_list: 待查找目录的列表
    filename_templates: 指定文件名模板的列表

    返回值:
    包含所有匹配的文件的列表

    """

    matching_files = []  # 存储匹配的文件列表

    for directory in directory_list:  # 遍历目录列表
        for root, dirs, files in os.walk(directory):  # 使用os.walk遍历目录及其下级目录
            for filename in files:  # 遍历目录下的每个文件
                for template in filename_templates:  # 遍历文件名模板列表中的每个模板
                    # 如果文件名与某个模板匹配，则将该文件的完整路径添加到结果列表中
                    if fnmatch.fnmatch(filename, template):
                        matching_files.append(os.path.join(root, filename))
    
    # 返回所有匹配文件的列表
    return matching_files
