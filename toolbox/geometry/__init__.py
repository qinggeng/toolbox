"""
几何数学相关
"""

################################################################################
def scale_dimensions(original_width, original_height, constraint_width, constraint_height):
  # 计算宽度和高度的缩放比例
  width_ratio = constraint_width / original_width
  height_ratio = constraint_height / original_height

  # 选择较小的缩放比例，以保持纵横比不变
  scale_ratio = min(width_ratio, height_ratio)

  # 根据缩放比例计算新的宽度和高度
  new_width = int(original_width * scale_ratio)
  new_height = int(original_height * scale_ratio)

  return new_width, new_height