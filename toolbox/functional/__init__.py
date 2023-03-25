import os
import os.path
from typing import Callable, Any

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

def inorder_traversal(root, condition_func: Callable[[Any], bool]) -> Any:
  """
  中序遍历一颗树，并使用判定函数判断当前节点是否符合条件。

  Args:
    root: 根节点对象
    condition_func: 判定函数，参数为节点的值，返回值为bool类型

  Returns:
    所有符合条件的节点对象(generater)

  Raises:
    TypeError: 如果root不是一个树节点对象或condition_func不是一个可调用对象

  Examples:

    >>> root = TreeNode(1, [TreeNode(2, [TreeNode(4)]), TreeNode(3)])
    >>> def condition(val):
    ...   return val > 2
    >>> for node in inorder_traversal(root, condition):
    ...   print(node.value)
    4
    3
  """
  if not callable(condition_func):
    raise TypeError("condition_func参数必须是一个可调用对象")

  visited = set() # 用于存储访问过的节点
  stack = [root]  # 用于模拟递归的栈

  while stack:
    current_node = stack.pop()
    if current_node not in visited:
      visited.add(current_node) # 加入visited中，标识已访问
      if not hasattr(current_node, 'children') or not current_node.children:
        # 如果当前节点没有children属性或children为空，则为叶节点
        if condition_func(current_node):
          yield current_node
      else:
        # 如果当前节点有children，则将children逆序加入stack中，这样可以实现中序遍历
        if condition_func(current_node):
          yield current_node
        for child in current_node.children[::-1]:
          stack.append(child)

