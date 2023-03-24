import subprocess

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