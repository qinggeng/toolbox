import re

def generate_toc_and_numbering(markdown_text):
    toc = generate_toc(markdown_text)  # 生成有序目录
    numbered_text = number_headings(markdown_text)  # 给章节标题加上序号

    toc_table = f"\n\n{toc}\n\n"  # 将目录表添加到markdown文本的标题下方
    numbered_text = re.sub(r'^(#\s.+\n)', rf'\1{toc_table}', numbered_text, flags=re.MULTILINE)  # 找到第一个标题，将目录表添加在它下方

    return numbered_text

def generate_toc(markdown_text):
    headings = re.findall(r"^(#+) (.+)$", markdown_text, flags=re.MULTILINE) # 提取所有标题

    toc = ""
    last_level = 0
    header_number = []

    for heading in headings:
        level, title = len(heading[0]), heading[1]
        title = add_header_number(title, header_number, level)

        toc += "  " * (level - 1) + "- " + f"[{title}](#{format_title(title)})\n"  # 目录项

        last_level = level

    return toc


def add_header_number(title, header_number, level):
    if len(header_number) >= level:  # 返回到新的标题级别
        header_number[level - 1] += 1  # 更新标题级别的数量
        header_number[level:] = [0] * (len(header_number) - level)
    else:  # 开始一个新的级别
        header_number += [1] * (level - len(header_number))
    return f"{'.'.join(str(x) for x in header_number)} {title}"

def format_title(title):
    return title.lower().replace(" ", "-").replace("'", "") # 标题格式化


def number_headings(markdown_text):
    headings = []
    for line in markdown_text.split("\n"):  # 提取所有的章节标题
        if line.startswith("#"):
            headings.append(line)

    data = []
    for h in headings:
        level = h.count("#")
        _, title = h.split(" ", 1)
        data.append((level, title.strip()))

    data.sort()  # 根据层级排序
    result = []

    last_numbers = [0] * (data[0][0] - 1)  # 从第一个标题开始。初始化为0
    for level, title in data:
        if level == data[0][0]:  # 如果层级是最顶层
            last_numbers = [1]  # 序号从1开始
        else:
            while level - data[0][0] > len(last_numbers) - 1:  # 检查序号长度是否正确
                last_numbers.append(1)  # 如果序号长度不足，添加一个新的序号
            if level - data[0][0] < len(last_numbers) - 1:  # 检查序号长度是否过长
                last_numbers = last_numbers[:level-data[0][0]]  # 如果序号长度过长，截断多余的项
            last_numbers[-1] += 1  # 最后一项加1

        numbered_title = f"{'.'.join([str(n) for n in last_numbers])} {title}\n"
        result.append(numbered_title)

    return re.sub(r"#+", f"{'#' * data[0][0]}", "\n".join(result))  # 替换原有标题


