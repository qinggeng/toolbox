"""
给过长的ass字幕换行
"""
import toolbox.functional as fp
from functools import partial
import toolbox.subtitles as sbs
from argparse import ArgumentParser

def script_main():
  parser = ArgumentParser()
  parser.add_argument("--length", default = 22, help = "每行字数限制")
  parser.add_argument("input_file", help = "要处理的ass文件")
  args = parser.parse_args()
  fp.transform_file(args.input_file, None, partial(sbs.reorganize_ass_subtitle, max_len = args.length))

if "__main__" == __name__:
  exit(script_main())