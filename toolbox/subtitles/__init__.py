import pysrt

def reorganize_ass_subtitle(content: str, max_len: int) -> str:
    """
    将输入的字幕文件内容重新排版后返回。

    参数：
    content: str -- 字幕文件内容字符串。
    max_len: int -- 一个整数，表示重新排版时最大的行宽度。

    返回：
    str -- 改变排版后的字符串内容。
    """
    lines = content.split('\n')
    for i in range(len(lines)):
        if lines[i].startswith('Dialogue:'):
            elements = lines[i].split(',', 9)
            dialogue = elements[9].replace('\\N', ' ')  # 去除换行标志
            lines[i] = ','.join(elements[:9]) + f',{insert_newlines(dialogue, max_len)}' # 插入重新计算的换行标志
    return '\n'.join(lines)


def insert_newlines(string: str, max_len: int) -> str:
    """
    将输入字符串中的换行标志重新调整。

    参数：
    string: str -- 字符串内容。
    max_len: int -- 一个整数，表示重新计算换行标志的宽度。

    返回：
    str -- 调整后的字符串内容。
    """
    new_string = ''
    for i in range(0, len(string), max_len):
        new_string += string[i:i + max_len].strip() + '\\N'
    return new_string[:-2]  # 去掉最后的换行标志

def get_srt_info(srt_string):
    """
    从 srt 字串中解析字幕信息

    Args:
        srt_string (str): 包含 srt 字幕的字符串

    Returns:
        list: 包含每个字幕的信息
            字幕项包括：
                subtitle: pysrt 字幕对象
                duration: 以秒为单位的持续时间
                prev_gap: 与前一项间隔时间，如果是第一个则为 None
                next_gap: 与下一项间隔时间，如果是最后一个则为 None
    """
    subs = pysrt.SubRipFile.from_string(srt_string)

    results = []
    prev_end = None

    for idx, sub in enumerate(subs):
        duration = sub.end - sub.start
        prev_gap = sub.start - prev_end if prev_end else None
        next_gap = subs[idx + 1].start - sub.end if idx + 1 < len(subs) else None

        results.append({
            "subtitle": sub,
            "duration": duration.total_seconds(),
            "prev_gap": prev_gap.total_seconds() if prev_gap else None,
            "next_gap": next_gap.total_seconds() if next_gap else None
        })

        prev_end = sub.end

    return results