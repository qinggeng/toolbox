import os
import argparse
from pydub import AudioSegment
from pydub.silence import split_on_silence

def merge_audio_segments(segments, min_duration):
    """
    合并多个音频片段为大于给定时长下限的音频片段。
    @param segments: 需要合并的音频片段列表。
    @param min_duration: 合并后的音频片段最小时长，单位为毫秒。
    @return: 合并后的音频片段列表。
    """
    merged_segments = []
    current_segment = None
    for segment in segments:
        if current_segment is None:
            current_segment = segment
        else:
            current_duration = len(current_segment)
            if current_duration < min_duration:
                current_segment += segment
            else:
                merged_segments.append(current_segment)
                current_segment = segment
    if current_segment is not None:
        merged_segments.append(current_segment)
    return merged_segments

################################################################################
# 创建参数解析器并解析参数
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True, help="输入音频文件的路径")
ap.add_argument("-o", "--output", default=None, help="输出目录的路径")
ap.add_argument("-s", "--silent", type=float, default=0.5, help="用于分割音频的最小静默时长（以秒为单位）")
ap.add_argument("--max", type=float, default=30, help="用于分割音频的最大时长（以秒为单位）")
ap.add_argument("--min", type=float, default=8, help="用于分割音频的最小时长（以秒为单位）")
ap.add_argument("--sample-rate", type = int, default = 16000, help="输出的采样频率")
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

# 定义最小时长
min_segment_len = int(args["min"] * 1000)

# 定义最大时长
max_segment_len = int(args["max"] * 1000)

# 根据静默时长将音频分割成多个块
chunks = split_on_silence(sound, 
                          min_silence_len=min_silence_len, 
                          keep_silence=min_silence_len/2,
                           silence_thresh=-60,
                           )
chunks = merge_audio_segments(chunks, min_segment_len)
# print(len(chunks))
# print(max([len(x) for x in chunks]))

# 导出每个块到单独的文件中（输出文件名格式为“文件名-块序号.wav”）
for i, chunk in enumerate(chunks):
    output_file_name = f"{os.path.splitext(input_file_name)[0]}-{i}.wav"
    output_file_path = os.path.join(output_dir_path, output_file_name)
    chunk.set_frame_rate(args["sample_rate"]).export(output_file_path, format="wav")
    
print(f"{len(chunks)}个音频块已经导出到目录：{output_dir_path}")
