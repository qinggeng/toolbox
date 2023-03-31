import subprocess
import os
import concurrent.futures

def ssh_execute_command(*, hostname, username=None, keypath=None, command=''):
  """
  通过 SSH 连接到远程主机，执行指定的命令，并返回执行结果。

  Args:
    hostname: 远程主机的 IP 地址或主机名。
    username: 要使用的用户名，如果未指定，则使用当前用户。
    keypath: SSH 密钥的路径，如果未指定，则使用系统默认密钥。
    command: 要执行的命令。

  Returns:
    返回一个包含标准输出、标准错误输出和返回码的元组。

  Raises:
    subprocess.SubprocessError: 如果 SSH 连接或命令执行失败。
  """
  # 创建 SSH 命令
  ssh_command = ['ssh']
  if username:
    ssh_command += [f'{username}@{hostname}']
  else:
    ssh_command += [hostname]
  if keypath:
    ssh_command += ['-i', f'{keypath}']
  ssh_command += [command]
  # 执行命令并读取输出和返回码
  p = subprocess.Popen(ssh_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  stdout_str, stderr_str = p.communicate()
  returncode = p.returncode
  # 将输出转换为字符串并删除末尾空格
  stdout_str = stdout_str.decode('utf-8').rstrip()
  stderr_str = stderr_str.decode('utf-8').rstrip()

  return (stdout_str, stderr_str, returncode)


def make_rsync_command(source_path, dest_path, exclude_list=None, delete=False, dry_run=False):
  """
  组织rsync命令

  Args:
    source_path: 源路径
    dest_path: 目标路径
    exclude_list: 排除文件的列表
    delete: 是否使用--delete选项
    dry_run: 是否使用--dry-run选项

  Returns:
    rsync命令
  """
  cmd = "rsync -av{0}{1} {2} {3}".format(
    " --delete" if delete else "",
    " --dry-run" if dry_run else "",
    source_path,
    dest_path
  )

  if exclude_list:
    exclude_options = ""
    for exclude in exclude_list:
      exclude_options += " --exclude '{0}'".format(exclude)
    cmd += exclude_options

  return cmd

def check_ssh_agent_running():
    """
    检查当前系统是否存在SSH代理。

    :return: 如果SSH代理正在运行，则返回True，否则返回False。
    """
    try:
        # 列出正在运行的进程
        output = subprocess.check_output(['ps', 'aux'])
        processes = output.decode('utf-8').split('\n')
        # 查找包含"ssh-agent"的进程
        ssh_agent_processes = [p for p in processes if 'ssh-agent' in p]
        # 如果找到一个"ssh-agent"进程，则代理正在运行
        return len(ssh_agent_processes) > 0
    except subprocess.CalledProcessError:
        # 如果无法列出进程，则假定SSH代理未运行
        return False

def add_ssh_key(ssh_key_str):
    """将ssh密钥添加到ssh-agent"""
    # 创建一个子进程并通过管道将ssh密钥字符串传递给ssh-add命令
    p = subprocess.Popen(['ssh-add', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # 将ssh密钥字符串写入输入流
    output, error = p.communicate(input=ssh_key_str.encode())

    # 检查是否成功添加密钥，并返回对应的 Boolean 值
    if p.returncode == 0:
        return True
    else:
        return False

def check_ssh_connectivity(ip_address: str, username: str) -> bool:
    """
    使用系统自带的 ssh 命令连接远程服务器，并检查连接是否成功。

    Args:
        ip_address: 要连接的远程服务器的 IP 地址
        username: 连接远程服务器所使用的用户名

    Returns:
        如果连接成功，返回 True；否则，返回 False。

    Raises:
        None
    """
    # 构建 ssh 命令
    ssh_cmd = ["ssh", f"{username}@{ip_address}", "-o", "ConnectTimeout=5", "-o", "BatchMode=yes", "echo", "Connected."]
    # 执行命令
    output = subprocess.run(ssh_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # 检查命令执行结果
    if output.returncode == 0 and b'Connected.' in output.stdout:
        return True
    else:
        return False

def run_commands(commands):
    """
    根据最大硬件线程数运行外部命令列表并返回结果。

    参数：
    commands -- 字符串列表，包含要运行的外部命令。

    返回值：
    包含 `(returncode, stdout, stderr, command)` 的元组列表，
    其中 `returncode` 是命令的返回码，`stdout` 和 `stderr` 是命令的输出和错误信息，`command` 是命令字符串。

    运行示例：
        >>> commands = ['echo "Hello world"', 'echo "How are you?"', 'echo "Goodbye"']
        >>> run_commands(commands)
        [(0, 'Hello world\n', '', 'echo "Hello world"'), (0, 'How are you?\n', '', 'echo "How are you?"'), (0, 'Goodbye\n', '', 'echo "Goodbye"')]
    """

    # 获取硬件线程数
    cpu_count = os.cpu_count()
    # 控制最大的并发度，即同时执行的进程的数量，避免超过硬件线程数，防止过度并发和资源饱和
    max_workers = min(cpu_count, len(commands))
    # 进程池对象
    pool = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
    # 每个进程的输出结果列表
    results = []

    # 通过进程池执行命令列表
    futures = [pool.submit(subprocess.Popen, cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) for cmd in commands]

    # 收集每个进程的输出
    for idx, future in enumerate(concurrent.futures.as_completed(futures)):
        # 取回每个进程的输出，使用 communicate() 方法获取 stdout 和 stderr 并转换为字符串
        stdout, stderr = future.result().communicate()
        returncode = future.result().returncode
        command = commands[idx]
        results.append((returncode, stdout.decode("utf-8"), stderr.decode("utf-8"), command))
        
    return results

import subprocess

def run_command(command):
  """
  执行一个命令，并将标准输出和标准错误输出作为生成器函数的返回值返回。
  
  参数：
  command：待执行的命令和参数列表，类型为 List[str]。
  
  返回值：
  生成器对象，每次调用生成器对象的 __next__() 方法或使用 for 循环获取子进程的输出，
  都会返回一个元组 (is_end, returncode, stdout, stderr)：
  - is_end：bool 类型，表示子进程是否已经完成。
  - returncode：int 类型，表示子进程的返回码。
  - stdout：str 类型，表示子进程的标准输出。
  - stderr：str 类型，表示子进程的标准错误输出。
  """
  # 执行命令，将标准输出和标准错误输出全部重定向到管道中
  p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

  while True:
    # 检查子进程是否完成
    poll_result = p.poll()

    # 读取子进程的标准输出和标准错误输出
    out = p.stdout.readline().decode('utf-8')
    err = p.stderr.readline().decode('utf-8')

    # 处理子进程的输出
    out = out.strip() if out is not None else ''
    err = err.strip() if err is not None else ''

    yield bool(poll_result is not None and not out and not err), \
          poll_result, \
          out, \
          err

    # 如果子进程已经完成并且输出已经读完，则退出循环
    if poll_result is not None and not out and not err:
      break

  # 子进程已经完成，读取最后一次标准输出和标准错误输出
  out, err = p.communicate()
  out = out.decode('utf-8').strip() if out is not None else ''
  err = err.decode('utf-8').strip() if err is not None else ''
  if out or err:
    yield True, p.returncode, out, err
