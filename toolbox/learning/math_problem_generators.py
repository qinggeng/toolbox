import random, ast, re
from functools import partial
from pprint import pprint as pp, pformat as pf

def generate_expression_pri(steps):
  operators = ['+', '-', '*', '/']
  expression = str(random.randint(1, 1000))
  for i in range(steps):
    op = random.choice(operators)
    num = random.randint(2, 100)
    expression += f' {op} {num}'
  return expression

class Node:
  def __init__(self, value):
    self.value = value
    self.left = None
    self.right = None

Node.add_children = lambda self, left, right: (setattr(self, 'left', left), setattr(self, 'right', right), self)[2]

def build_expression_tree(expression):
  """
  构建表达式树

  Args:
    expression (str): 表达式字符串

  Returns:
    Node: 表达式树的根节点
  """
  def build_tree(node):
    if isinstance(node, ast.Num):
      return Node(node.n)
    elif isinstance(node, ast.BinOp):
      op = node.op.__class__.__name__
      left = build_tree(node.left)
      right = build_tree(node.right)
      return Node(op).add_children(left, right)
    else:
      raise TypeError(f'Unsupported node type: {type(node).__name__}')

  ast_tree = ast.parse(expression, mode='eval')
  root = build_tree(ast_tree.body)
  return root

def evaluate_expression_tree(node, validator = None):
  """
  计算表达式树的值。

  Args:
    node (Node): 表达式树的根节点。
    validator (callable, optional): 一个验证器函数，用于验证计算结果。默认为None。

  Returns:
    float: 计算结果。

  Raises:
    ValueError: 不支持的运算符。

  Examples:
    >>> node = Node('Add')
    >>> node.left = Node(3)
    >>> node.right = Node(5)
    >>> evaluate_expression_tree(node)
    8
  """
  if node.left is None and node.right is None:
    return node.value
  left_value = evaluate_expression_tree(node.left, validator)
  right_value = evaluate_expression_tree(node.right, validator)
  if None != validator:
    validator(node.value, left_value, right_value)
  if node.value == 'Add':
    result = left_value + right_value
  elif node.value == 'Sub':
    result = left_value - right_value
  elif node.value == 'Mult':
    result = left_value * right_value
  elif node.value == 'Div':
    result = left_value / right_value
  else:
    raise ValueError(f'Unsupported operator: {node.value}')
  return result

def validate_calc(op, l, r):
  """
  按照规则验证计算表达式，规则：
  - 左右两边都是正整数
  - 计算结果为正整数
  - 除法的场合，除数不能为0, 不能大于20
  - 乘法的结果不能大于5000
  如果违反规则，则抛出ValueError异常
  """
  op_map = dict(Div='/', Mult='*', Add='+', Sub='-')
  if int(l) != l or int(r) != r:
    raise ValueError("Left and right operands must be positive integers")
  if op == "Div" and (r == 0 or r > 20):
    raise ValueError("Divisor must be a non-zero positive integer less than or equal to 20")
  if op == "Mult" and l * r > 5000:
    raise ValueError("Product of operands must be less than or equal to 5000")
  if op != "Add" and op != "Sub" and op != "Mult" and op != "Div":
    raise ValueError("Invalid operation")
  if op == "Div" and l / r <= 0:
    raise ValueError("Division result must be a positive integer")
  ret = eval(f"{l} {op_map[op]} {r}")
  if int(ret) != ret or ret < 0:
    raise ValueError("Invalid result")

def validate_and_collect(s, o, l, r):
  op_map = dict(Div='/', Mult='*', Add='+', Sub='-')
  op_print_map = dict(Div='÷', Mult='×', Add='+', Sub='-')
  validate_calc(o, l, r)
  ret = eval(f"{l} {op_map[o]} {r}")
  s.append(f"{int(l):>4} {op_print_map[o]} {int(r):<4} = {int(ret)}")

def print_expression_tree(node):
  if node is None:
    return
  print(node.value)
  print_expression_tree(node.left)
  print_expression_tree(node.right)


def make_quesstion(steps_count = 6):
  generated = False
  while not generated:
    try:
      steps = []
      expression = generate_expression_pri(steps_count)
      expression = add_parentheses(expression)
      if "/" not in expression:
        continue
      expression = re.sub(r"\(\s*(\d+)\s*\)", r"\1", expression)

      node = build_expression_tree(expression)
      # print_expression_tree(node)
      evaluate_expression_tree(node, partial(validate_and_collect, steps))
      generated = True
      return dict(expression = expression, steps = steps)
    except ValueError:
      pass
    except:
      pass
  
def print_expression():
  """
  打印表达式并执行相关操作。

  生成一个表达式，然后构建表达式树，并执行验证和收集操作。
  最后打印表达式和收集到的步骤。

  Args:
    None

  Returns:
    None
  """
  question = make_quesstion(6)
  question_txt = question['expression']
  print(question_txt)
  steps = question['steps']
  print("\n".join(steps))

def random_bracket(tokens, open_prob = 0.2, close_prob = 0.5):
  offset = 0
  open_offset = -1
  close_offset = -1
  for offset, (token_type, value) in enumerate(tokens):
    if token_type not in set(['num', 'expr']):
      offset += 1
      continue
    if open_offset == -1:
      if random.random() > open_prob:
        open_offset = offset
    elif close_offset == -1:
      if random.random() > close_prob:
        close_offset = offset + 1
        break
  if open_offset != -1 and close_offset == -1:
    open_offset = -1
  return (open_offset, close_offset)

def split_list(lst, indices):
    """
    根据给定的索引二元组，将列表分成三段。

    Args:
        lst (list): 输入的列表。
        indices (tuple): 索引的起点和终点二元组。

    Returns:
        tuple: 分割后的三段列表。
    """
    start, end = indices
    segment1 = lst[:start]
    segment2 = lst[start: end]
    segment3 = lst[end:]
    return segment1, segment2, segment3

def make_token_array(expression):
  """
  将表达式转化为令牌数组。

  Args:
    expression (str): 表达式字符串。

  Returns:
    List[Tuple[str, str]]: 令牌数组，每个令牌由类型和值组成的元组。

  """
  n = re.compile(r"(?P<num>\d+)")
  op = re.compile(r"(?P<op>[\+\-\*\/])")
  lp = re.compile(r"(?P<lp>[\(\)])")
  rp = re.compile(r"(?P<rp>[\)])")
  token = n.pattern + '|' + op.pattern + '|' + lp.pattern + '|' + rp.pattern
  tokens = re.findall(token, expression)
  token_types = ["num", "op", "lp", "rp"]
  tokens = [[(token_type, value) for token_type, value in zip(token_types, t) if value != ''][0] for t in tokens]
  return tokens


def add_parentheses(expression, level = 2):
  """
  随机给四则运算表达式加上括号。

  在给定的四则运算表达式上随机添加括号，并返回添加括号后的表达式。

  Args:
    expression (str): 四则运算表达式字符串。

  Returns:
    str: 添加括号后的表达式字符串。
  """
  tokens = make_token_array(expression)
  for i in range(level):
    tokens = add_brackets(tokens)
    # print(tokens)
  return " ".join([v for t, v in tokens]) 

def add_brackets(tokens, try_count = 2):
  ret = []
  for i in range(try_count):
    bracket = random_bracket(tokens)
    tail = []
    if bracket != (-1, -1):
      head, expr, tail = split_list(tokens, bracket)
      if len(head) > 0:
        ret += head
      if len(expr) > 0:
        ret += [('expr', f"( {' '.join([v for t, v in expr])} )")]
      tokens = tail
  if len(tokens) > 0:
    ret += tokens
  return ret

# generate_expression = generate_expression_pri
# print(add_parentheses(generate_expression_pri(6)))
# print_expression()