from toolbox.fs import search_files

def test_search_files():
    # 测试能否正确找到文件
    result = search_files(start_dir='.', file_name='test_fs_tools.py', skip_dirs=[])
    assert result['.'] == None
    assert result['./toolbox'] == None
    assert result['./tests'] == './tests/test_fs_tools.py'

    # 测试跳过指定目录
    result = search_files(start_dir='.', file_name='test_fs_tools.py', skip_dirs=['tests'])
    assert './tests' not in result

    # 测试找不到文件的情况
    result = search_files(start_dir='.', file_name='not_exist.py', skip_dirs=['venv'])
    assert False == any(result.values())