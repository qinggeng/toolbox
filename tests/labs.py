# 实验无边框文字绘制
# ===============
# ===============

# from toolbox.images import *
# import os.path as path
# font_file_path = path.join(path.dirname(__file__), "smiley-sans-v1.1.1/SmileySans-Oblique.otf")
# txt = """
# 中文多行混测
# abc
# 123
# +_)()
# """.strip()
# i = draw_text(txt, font_size=72, font_file=font_file_path, color = (255, 255, 255))
# bbox = i.getbbox()
# i = i.crop(bbox)
# # print(get_bounding_box(i))
# i.save("sample.png")

# 实验汉字的ASCII-ART
# ===============
# ===============

def get_pixel_char(p, threshhold):
  r,g,b,a = p
  if a > threshhold:
    return "#"
  return " "

from toolbox.images import *
from PIL import ImageOps
import os.path as path
font_file_path = path.join(path.dirname(__file__), "smiley-sans-v1.1.1/SmileySans-Oblique.otf")
txt = """
A\u2009S\u2009C\u2009I\u2009I
""".strip()
txt = """
看\u2009图
""".strip()

for threshhold in [0, 20, 40, 80, 100, 120, 140, 160, 200]:
  print(f"threshholde = {threshhold}")
  ascii_txt = txt2asciiart(txt, 12, font_file_path, threshhold)
  print(ascii_txt)