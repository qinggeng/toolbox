import toolbox.learning.math_problem_generators as mpg
from PIL import ImageFont, ImageDraw, Image
from pprint import pprint as pp
import os.path as path
from toolbox.images import extend_image, split_paper, a4_vertical_size
from toolbox.geometry import scale_dimensions


########################################
#       class QuestionFormatter        #
########################################
class QuestionFormatter(object):

  ##############################################################################
  def __init__(self, 
               *, 
               font_file_path,
               font_size = 12,
               color = (0, 0, 0)):
    self._font_file_path = font_file_path
    self._font_size = font_size
    self._color = color
    if None != self._font_file_path:
      self._font = ImageFont.truetype(self._font_file_path, self._font_size)
  
  ##############################################################################
  @property
  def font_file_path(self):
    return self._font_file_path

  ##############################################################################
  @font_file_path.setter
  def font_file_path(self, value):
    if (not isinstance(value, str)):
      raise TypeError('font_file_path must be a string')
    if self._font_file_path == value:
      return
    self._font_file_path = value
    self._font = ImageFont.truetype(self._font_file_path, self._font_size)

  ##############################################################################
  @property
  def font_size(self):
    return self._font_size
  
  ##############################################################################
  @font_size.setter
  def font_size(self, value):
    if (not isinstance(value, int)):
      raise TypeError('font_size must be an integer')
    if self._font_size == value:
      return
    self._font_size = value
    self._font = ImageFont.truetype(self._font_file_path, self._font_size)

  ##############################################################################
  @property
  def color(self):
    return self._color
  
  ##############################################################################
  @color.setter
  def color(self, value):
    if (not isinstance(value, tuple)):
      raise TypeError('color must be a tuple')
    if self._color == value:
      return
    self._color = value

  ############################################################################
  def draw_txt(self, *, text):
    """
    绘制文本并返回包含文本的图像对象。
    
    参数选拉
    text (str): 要绘制的文本。
    """
    # 计算图片大小
    font = self._font
    text_width, text_height = font.getsize(text)
    image_size = (text_width+1, (text_height+1) * (text.count('\n') + 1 ))
    image = Image.new("RGBA", image_size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    draw.multiline_text((0, 0), text, font = font, fill = self._color)
    bbox = image.getbbox()
    image = image.crop(bbox)
    return image

########################################
#              FUNCTIONS               #
########################################
################################################################################
def make_answer_image(question, index):
  expr = question['expression']
  steps = question['steps']
  step_txt = '\n'.join(steps)
  txt = f"{index}.   {expr}\n解题步骤：\n{step_txt}"
  fmt = QuestionFormatter(font_file_path = path.join(path.dirname(__file__), "smiley-sans-v1.1.1/SmileySans-Oblique.otf"), font_size = 72, color = (0, 0, 0))
  return fmt.draw_txt(text = txt)

################################################################################
def make_question_image(question, index):
  expr = question['expression']
  txt = f"{index+1:#2}.   {expr}"
  fmt = QuestionFormatter(font_file_path = path.join(path.dirname(__file__), "smiley-sans-v1.1.1/SmileySans-Oblique.otf"), font_size = 72, color = (0, 0, 0))
  return fmt.draw_txt(text = txt)

################################################################################
def row_to_column(array, rows, cols):
  column_array = []
  for col in range(cols):
    for row in range(rows):
      index = col + row * cols
      column_array.append(array[index])
  return column_array

################################################################################
def make_single_question_image(question, index):
  question_img = make_question_image(question, index)
  question_img = extend_image(question_img, ratio_h=1.05, ratio_w=1.3)
  quiz_size = question_img.size
  # quiz_size = (quiz_size[0] + 20, quiz_size[1] + 20)
  quiz_img = Image.new("RGBA", quiz_size, (255, 255, 255, 255))
  r, g, b, a = question_img.split()
  mask = a.point(lambda x: 255 if x > 0 else 0)
  quiz_img.paste(question_img, (0, 0), mask = mask)
  return quiz_img

################################################################################
def make_single_answer_image(answer, index):
  answer_img = make_answer_image(answer, index)
  answer_img = extend_image(answer_img, ratio_h=1.05, ratio_w=1.3)
  quiz_size = answer_img.size
  # quiz_size = (quiz_size[0] + 20, quiz_size[1] + 20)
  quiz_img = Image.new("RGBA", quiz_size, (255, 255, 255, 255))
  r, g, b, a = answer_img.split()
  mask = a.point(lambda x: 255 if x > 0 else 0)
  quiz_img.paste(answer_img, (0, 0), mask = mask)
  return quiz_img


################################################################################
def make_single_quiz(prefix):
  count = 10
  questions = [mpg.make_quesstion() for _ in range(count)]
  rects = split_paper(rows = 5, columns = 2)
  rects = row_to_column(rects, 5, 2)
  quiz_image = Image.new("RGBA", a4_vertical_size, (255, 255, 255, 255))
  answer_image = Image.new("RGBA", a4_vertical_size, (255, 255, 255, 255))
  for i, (r, q) in enumerate(zip(rects, questions)):
    img = make_single_question_image(q, i)
    x1, y1, x2, y2 = r
    new_size = scale_dimensions(img.size[0], img.size[1], x2 - x1, y2 - y1)
    img = img.resize(new_size)
    quiz_image.paste(img, (x1, y1))
    img_answer = make_single_answer_image(q, i)
    new_size = scale_dimensions(img_answer.size[0], img_answer.size[1], x2 - x1, y2 - y1)
    print(img_answer.size, new_size)
    img_answer = img_answer.resize(new_size)
    answer_image.paste(img_answer, (x1, y1))
  quiz_image = quiz_image.resize((quiz_image.size[0]//2, quiz_image.size[1]//2))
  quiz_image.save(f'{prefix}-quiz.pdf')
  answer_image = answer_image.resize((answer_image.size[0]//2, answer_image.size[1]//2))
  answer_image.save(f'{prefix}-answer.pdf')

for i in range(4):
  make_single_quiz(f'quiz{i+1}')