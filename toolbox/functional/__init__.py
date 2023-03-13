import os
import os.path

def transform_file(input_path: str, output_path: str = None, process_func=None) -> None:
    """
    读取输入路径文件内容，并经过处理函数处理后将结果写入输出路径文件中。

    参数：
    input_path: str -- 字符串，表示输入路径。
    output_path: str -- 字符串，表示输出路径，默认为None。
    process_func: function -- 处理输入内容和返回处理后的内容的函数对象。

    返回：
    None

    Raises:
    TypeError: 如果输入参数类型不正确，将引发 TypeError 异常。
    FileNotFoundError: 如果输入路径对应的文件不存在，将引发 FileNotFoundError 异常。

    """
    # 检查输入参数类型是否正确
    if not isinstance(input_path, str) or (output_path is not None and not isinstance(output_path, str)) \
            or not callable(process_func):
        raise TypeError('transform_file(): input_path and output_path must be str or None, and process_func must be callable.')

    # 检查文件是否存在
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"transform_file(): Input file {input_path} does not exist.")

    # 如果输出路径为 None，则在输入路径的文件名上添加.out后缀
    if output_path is None:
        base_path, ext = os.path.splitext(input_path)
        output_path = base_path + '.out' + ext

    # 读取输入文件内容
    with open(input_path, 'r', encoding='utf-8') as f:
        input_content = f.read()

    # 处理输入内容
    output_content = process_func(input_content)

    # 将处理结果写入输出文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output_content)