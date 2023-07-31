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

def remove_border(image: Image) -> Image:
  """
  去除图片边框。

  Args:
      image: PIL Image 对象。

  Returns:
      去除图片边框后的 Image 对象。
  """
  bbox = image.getbbox()
  return image.crop(bbox)

def extend_image(image: Image, 
                  *, 
                  ratio_h, 
                  ratio_w, 
                  color = (0, 0, 0, 0), 
                  mask = None)->Image:
  """
  增加图片边框。

  Args:
      image: PIL Image 对象。
      ratio_h: 图片高度的比例。
      ratio_w: 图片宽度的比例。
      color: 边框颜色。
      mask: 图像掩码。
  """
  orig_sz = image.size
  w, h = orig_sz
  new_h, new_w = int(h * ratio_h), int(w * ratio_w)
  new_sz = (new_w, new_h)
  new_image = Image.new('RGBA', new_sz, color)
  paste_x = int((new_sz[0] - w) / 2)
  paste_y = int((new_sz[1] - h) / 2)
  new_image.paste(image, (paste_x, paste_y), mask = mask)
  return new_image

a4_vertical_size = (2481, 3507)
a4_horizontal_size = (3507, 2481)
a4_vertical_padding = 177
a4_horizontal_padding = 167

def divide_rectangle(x1, y1, x2, y2, cols, rows):
  rectangle_list = []
  width = abs(x2 - x1)
  height = abs(y2 - y1)
  col_width = width / cols
  row_height = height / rows

  for row in range(rows):
    for col in range(cols):
      left = int(x1 + col * col_width)
      top = int(y1 + row * row_height)
      right = int(left + col_width)
      bottom = int(top + row_height)
      rectangle_list.append((left, top, right, bottom))

  return rectangle_list

def split_paper(
    *,
    rows,
    columns,
    page_size = a4_vertical_size,
    paddings = (a4_horizontal_padding, a4_vertical_padding),
  ):
  top_left = (paddings[0], paddings[1])
  bottom_right = (page_size[0] - paddings[0], page_size[1] - paddings[1])
  return divide_rectangle(
    top_left[0],
    top_left[1],
    bottom_right[0],
    bottom_right[1],
    columns,
    rows
  )