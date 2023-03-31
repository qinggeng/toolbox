import pytest, subprocess
from toolbox.shell import make_rsync_command
from toolbox.shell import make_rsync_command
from toolbox.shell import run_command

def test_make_rsync_command():
  source_path = '/path/to/source'
  dest_path = '/path/to/dest'
  exclude_list = ['.git', '.svn']
  delete = True
  dry_run = True

  expected_cmd = "rsync -av --delete --dry-run /path/to/source /path/to/dest --exclude '.git' --exclude '.svn'"
  assert make_rsync_command(source_path, dest_path, exclude_list, delete, dry_run) == expected_cmd

  exclude_list = None
  delete = False
  dry_run = False

  expected_cmd = "rsync -av /path/to/source /path/to/dest"
  assert make_rsync_command(source_path, dest_path, exclude_list, delete, dry_run) == expected_cmd

  exclude_list = ['.git', '.svn']
  delete = False
  dry_run = False

  expected_cmd = "rsync -av /path/to/source /path/to/dest --exclude '.git' --exclude '.svn'"
  assert make_rsync_command(source_path, dest_path, exclude_list, delete, dry_run) == expected_cmd

  exclude_list = None
  delete = True
  dry_run = False

  expected_cmd = "rsync -av --delete /path/to/source /path/to/dest"
  assert make_rsync_command(source_path, dest_path, exclude_list, delete, dry_run) == expected_cmd

  exclude_list = None
  delete = False
  dry_run = True

  expected_cmd = "rsync -av --dry-run /path/to/source /path/to/dest"
  assert make_rsync_command(source_path, dest_path, exclude_list, delete, dry_run) == expected_cmd

  exclude_list = ['.git', '.svn']
  delete = True
  dry_run = False

  expected_cmd = "rsync -av --delete /path/to/source /path/to/dest --exclude '.git' --exclude '.svn'"
  assert make_rsync_command(source_path, dest_path, exclude_list, delete, dry_run) == expected_cmd

def test_run_command_output():
    result = list(run_command(['echo', 'hello']))
    assert any(r[0] for r in result)

def test_run_command_error():
    assert list(run_command(['cat', 'nonexistent-file']))[-1][1] != 0

def test_run_command_timeout():
    result = list(run_command(['sleep', '2']))
    assert result[0] == (False, None, '', '')
    assert any(r[0] for r in result[1:])