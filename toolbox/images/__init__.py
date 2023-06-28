from PIL import Image, ImageDraw, ImageFont

def draw_text(text, font_size=12, font_file=None, color=(0, 0, 0)):
  """
  绘制文本并返回包含文本的图像对象。
  
  参数：
  text (str): 要绘制的文本。
  font_size (float): 文本字体大小（单位为点），默认值为12。
  font_file (str): 字体文件路径，默认值为None，表示使用默认字体。
  color (tuple): 文本颜色，以RGB元组形式表示（如(255, 0, 0)即为红色）。默认值为黑色。
  
  返回：
  包含绘制文本的图像对象。
  """
  # 计算图片大小
  # font = ImageFont.truetype(font_file, pt_to_px(font_size)) if font_file else ImageFont.load_default()
  print(font_size)
  font = ImageFont.truetype(font_file, font_size) if font_file else ImageFont.load_default()
  text_width, text_height = font.getsize(text)
  image_size = (text_width+1, (text_height+1) * (text.count('\n') + 1 ))

  # 创建新图片（透明背景）
  image = Image.new("RGBA", image_size, (255, 255, 255, 0))

  # 获取图片的Draw对象并绘制文字
  draw = ImageDraw.Draw(image)
  # draw.text((0, 0), text, font=font, fill=color)
  draw.multiline_text((0, 0), text, font = font, fill = color)

  return image

def pt_to_px(font_size_pt, dpi=72):
  """
  将字体大小从点（pt）转换为像素（px）。
  
  参数：
  font_size_pt (float): 字体大小，单位为点（pt）。
  dpi (int): 屏幕或打印机的分辨率，默认值为72dpi。
  
  返回：
  转换后的像素大小（整数）。
  """
  return int(font_size_pt * dpi / 72.0 + 0.5)

from PIL import Image

def get_bounding_box(image: Image) -> tuple:
  """
  给定一个 PIL Image 对象，返回其不透明部分的最大包围盒坐标。

  Args:
      image: PIL Image 对象。

  Returns:
      一个四元组 (x_min, y_min, x_max, y_max)，表示最大包围盒的左上角和右下角坐标。
  """
  # 获取 alpha 通道值数组
  alpha_values = image.getchannel('A').getdata()

  # 将 alpha 值小于 255（即不透明）的像素点设为 False，其余设为 True
  alpha_mask = [(alpha < 255) for alpha in alpha_values]

  # 将 alpha_mask 转换为二维列表
  alpha_mask_2d = [alpha_mask[i:i+image.width] for i in range(0, len(alpha_mask), image.width)]

  # 初始化最大包围盒的坐标
  x_min, y_min, x_max, y_max = None, None, None, None

  # 遍历每一行
  for i, row in enumerate(alpha_mask_2d):
    if not any(row):  # 如果这一行都是 False，则跳过
      continue

    # 找到这一行中第一个为 True 的像素点
    x_start = row.index(True)

    # 找到这一行中最后一个为 True 的像素点
    x_end = len(row) - 1 - row[::-1].index(True)

    # 更新最大包围盒的坐标
    if x_min is None or x_start < x_min:
      x_min = x_start
    if x_max is None or x_end > x_max:
      x_max = x_end

    if y_min is None:
      y_min = i
    if y_max is None or i > y_max:
      y_max = i

  return x_min, y_min, x_max, y_max
