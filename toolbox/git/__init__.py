import subprocess

def get_commit_info(filename):
  """
  获取指定文件中每行代码的作者、提交时间和代码内容。

  参数:
  filename (str): 要分析的文件名。

  返回值:
  list of (str, str, str): 由元组组成的列表，每个元组表示某一行的作者，提交时间和代码内容。

  示例：
  >>> get_commit_info("test.py")
  [('Tom Smith', '2019-01-01 08:00:00 (-0400)', 'print("Hello, World!")'), ('John Doe', '2019-01-02 12:00:00 (-0400)', 'for i in range(10):'), ('John Doe', '2019-01-02 12:02:00 (-0400)', '  print(i)')]
  """
  # 执行 git 命令
  cmd = ["git", "blame", "--date=short", filename]
  result = subprocess.check_output(cmd).decode().split("\n")
  
  # 解析结果
  commit_info = []
  for line in result:
    if not line.strip():
      continue
    # 每一行都会以此格式开头：commit_hash author_name date time tz_offset line_content
    # 我们通过字符串的分割来提取每个数据项
    # 顺序就是：commit_hash -> 作者名(author_name) -> 日期(date) -> 时间(time) -> 时区偏移(tz_offset) -> 代码行(line_content)
    commit_hash, author_name, date, time, tz_offset, *content = line.split()
    # 由于作者名前后都有括号，我们需要去掉它们来提取纯粹的作者名称
    author = author_name.lstrip("(").rstrip(")")
    # 将日期、时间和时区偏移组合为一个字符串
    commit_date = f"{date} {time} ({tz_offset})"
    # 将代码行内容连接为一个字符串
    content = " ".join(content)
    # 为每一条记录组装为 元组 (author, commit_date, content) ，并添加到 commit_info 列表中
    commit_info.append((author, commit_date, content))
  
  return commit_info

def get_user_files():
    """
    获取当前 Git 仓库下当前用户提交过的文件列表
    :return: 提交文件列表
    """
    # 使用 Git 命令列出当前用户提交过的所有文件，并将输出作为字符串返回
    cmd = "git log --author=$(git config user.name) --pretty=format: --name-only | sort -u"
    output = subprocess.check_output(cmd, shell=True, encoding="utf-8").splitlines()
    
    # 将输出字符串分割为一行行的列表并返回
    return output