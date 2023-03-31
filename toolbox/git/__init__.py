import subprocess
import re

def extract_commit_info(line: str) -> dict:
    """
    通过正则表达式从字符串中提取commit信息

    Args:
        line: 包含commit信息的字符串.

    Returns:
        包含commit信息的字典对象或None
    """

    regex = r'^([^\s]+)\s\((.*?)\s+(\d{4}-\d{2}-\d{2})\s+(\d+)\)\s(.*)$'
    match = re.match(regex, line)
    if match:
        commit_hash = match.group(1)
        author = match.group(2)
        date = match.group(3)
        line_no = match.group(4)
        content = match.group(5)
        return {'commit_hash': commit_hash, 'author': author, 'date': date,
                'line_no': line_no, 'content': content}
    else:
        return None
import shutil

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
  print(" ".join(cmd))
  result = subprocess.check_output(cmd).decode().strip().split("\n")
  
  # 解析结果
  commit_info = []
  for line in result:
    commit_info.append(extract_commit_info(line))
  return commit_info

def get_user_files():
    """
    获取当前 Git 仓库下当前用户提交过的文件列表
    :return: 提交文件列表
    """
    # 使用 Git 命令列出当前用户提交过的所有文件，并将输出作为字符串返回
    cmd = "git log --author=$(git config user.name) --pretty=format: --name-only | sort -u"
    output = subprocess.check_output(cmd, shell=True, encoding="utf-8").strip().splitlines()
    
    # 将输出字符串分割为一行行的列表并返回
    return output

def git_changed_files():
    """
    使用Git命令列出所有有变更和新添加的文件列表，但不显示被删除的文件。
    :return: 一个字符串列表，包含所有Git中被修改或新添加的文件。
    """
    command = "git status --short | grep '^ M\\|^A'"

    # 运行Git命令并捕获输出和错误信息
    output = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # 检查Git命令是否运行成功
    if output.returncode != 0:
        # 如果命令运行失败，则将错误信息解码为字符串并引发异常。
        error_message = output.stderr.decode().strip()
        raise RuntimeError(f"Error running Git command. Error: {error_message}")

    # 如果Git命令成功运行，则按空格拆分标准输出字符串并返回文件列表。
    changed_files = output.stdout.decode().split()
    return changed_files

def list_untracked_files():
    """
    找出 Git 仓库中未被跟踪的文件，并返回文件名列表。
    
    Returns:
        List[str]: 未被跟踪的文件名列表
    
    Examples:
        >>> untracked_files()
        ['example.txt', 'example_dir/sample.txt']
    """
    # 执行 shell 命令来获取未被跟踪的文件列表
    command = 'git status --porcelain | grep "^??" | cut -c4-'
    output = subprocess.run(command, shell=True, capture_output=True, text=True).stdout.strip().split('\n')
    
    untracked_files = []
    for file in output:
        if os.path.isdir(file):
            # 如果这个文件是目录，则递归处理其中的文件
            sub_files = [os.path.join(file, f) 
                         for f in os.listdir(file) 
                         if os.path.isfile(os.path.join(file, f))]
            untracked_files.extend(sub_files)
        else:
            # 如果这个文件不是目录，则直接添加到未被跟踪文件列表中
            untracked_files.append(file)
    return untracked_files

def list_unpushed_files(remote='origin', branch='master'):
    """
    列出当前分支中已经commit但是还未push到远程仓库的文件列表。

    Args:
        remote: 远程仓库的名称，默认为 'origin'
        branch: 要对比的远程分支名称，默认为 'master'

    Returns:
        未push的文件名列表
    """
    # 使用subprocess模块执行git命令
    diff_cmd = f"git log {remote}/{branch}..HEAD --name-only --pretty=format: | sort | uniq"
    result = subprocess.run(diff_cmd, stdout=subprocess.PIPE, shell = True)
    # 获取输出并以换行符分隔
    output_lines = result.stdout.decode('utf-8').strip().splitlines()
    # 返回结果列表
    return output_lines
def git_clone_and_move_dir(*, github_account=None, github_token=None, git_url, src_dir, dest_dir, branch=None):
    """
    克隆 Git 仓库，并移动指定目录到另一个目录

    Arguments:
    * -- 使用关键字参数传递
    github_account -- 您的 GitHub 账号名（可选）
    github_token -- 您的 GitHub 账号 token（可选）
    git_url -- 需要克隆的 Git 仓库地址
    src_dir -- 需要移动的目录路径
    dest_dir -- 目标目录路径
    branch -- 需要克隆的分支名称，默认为 Git 仓库的默认分支名称

    Returns:
    无返回值，执行完毕后将会克隆 Git 仓库，移动指定目录，并删除克隆的本地工作目录
    """

    # 添加 GitHub 账号认证信息，如果没有提供账号信息，则表示是克隆公开仓库
    if github_account and github_token:
        auth = f"{github_account}:{github_token}"
        auth_str = f"{auth}@"
        git_url = git_url.replace("https://", f"https://{auth_str}")

    # 克隆 Git 仓库到一个临时目录
    tmp_dir = "/tmp/git_clone_tmp"
    if branch:
        subprocess.run(["git", "clone", "-b", branch, git_url, tmp_dir])
    else:
        subprocess.run(["git", "clone", git_url, tmp_dir])

    # 移动指定目录到目标目录
    src_path = f"{tmp_dir}/{src_dir}"
    shutil.move(src_path, dest_dir)

    # 删除克隆的工作目录
    shutil.rmtree(tmp_dir)
