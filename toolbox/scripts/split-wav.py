import os
import argparse
from pydub import AudioSegment
from pydub.silence import split_on_silence

# 创建参数解析器并解析参数
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True, help="输入音频文件的路径")
ap.add_argument("-o", "--output", default=None, help="输出目录的路径")
ap.add_argument("-s", "--silent", type=float, default=0.5, help="用于分割音频的最小静默时长（以秒为单位）")
args = vars(ap.parse_args())

# 获取输入音频的路径和文件名
input_file_path = args["input"]
input_file_name = os.path.basename(input_file_path)

# 获取输出目录的路径。如果未提供输出目录，则默认输出到输入文件所在的目录。
if args["output"] is None:
    output_dir_path = os.path.dirname(input_file_path)
else:
    output_dir_path = args["output"]

# 创建输出目录（如果该目录不存在）
if not os.path.exists(output_dir_path):
    os.makedirs(output_dir_path)

# 将输入音频加载到PyDub中
sound = AudioSegment.from_file(input_file_path)

# 定义用于分割音频的最小静默时长
min_silence_len = int(args["silent"] * 1000)  # 将秒转换为毫秒

# 根据静默时长将音频分割成多个块
chunks = split_on_silence(sound, 
                          min_silence_len=min_silence_len, 
                          keep_silence=min_silence_len/2,
                           silence_thresh=-60,
                           )
print(len(chunks))

# 导出每个块到单独的文件中（输出文件名格式为“文件名-块序号.wav”）
for i, chunk in enumerate(chunks):
    output_file_name = f"{os.path.splitext(input_file_name)[0]}-{i}.wav"
    output_file_path = os.path.join(output_dir_path, output_file_name)
    chunk.export(output_file_path, format="wav")
    
print(f"{len(chunks)}个音频块已经导出到目录：{output_dir_path}")
