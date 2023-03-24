from toolbox.shell import make_rsync_command

import pytest
from toolbox.shell import make_rsync_command

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
