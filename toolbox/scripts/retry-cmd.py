#!/usr/bin/env python
import os
import sys


def try_run_command(retries: int, command: str) -> int:
  """
  反复执行命令，若干次直到成功或者超出次数限制。

  :param retries: 最多尝试执行的次数，-1 表示不限制尝试次数。
  :param command: 要执行的命令。
  :return: 如果执行成功则返回 0，否则返回 1。
  """
  counter = 1
  while retries == -1 or counter <= retries:
    print(f"Attempt {counter}:")
    return_code = os.system(command)
    if return_code == 0:
      print("Command succeeded.")
      return 0
    print("Command failed.")
    counter += 1
  print(f"Command failed after {counter - 1} attempts.")
  return 1


def main() -> None:
  # 处理命令行参数
  if len(sys.argv) < 3 or sys.argv[1] == "--help":
    print("用法: retry-cmd.py RETRIES COMMAND")
    print("  RETRIES: 最多尝试执行的次数，-1 表示不限制尝试次数。")
    print("  COMMAND: 要执行的命令。")
    return
  retries = int(sys.argv[1])
  command = sys.argv[2]
  # 执行命令
  try_run_command(retries, command)


if __name__ == '__main__':
  exit(main())