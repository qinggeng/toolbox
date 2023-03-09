def sep(input_val, sep=" ", sep_len=4):
    """
    将数字或字符串格式化，以指定的分隔长度和分隔符分隔。

    Args:
        input_val: 数字或字符串
        sep: 分隔符，默认为一个空格。
        sep_len: 将字符串分隔成的长度。默认为4。

    Returns:
        已经格式化的字符串

    Examples:
        >>> sep(123456789, "-", 3)
        '123-456-789'
        >>> sep('abcdefghij')
        'abcd efgi j'
    """
    # 把数字或字符串先转化为字符串类型
    input_val = str(input_val)[::-1]

    # 根据指定的sep_len对输入的字符串进行分片
    formatted_input = [input_val[i: i+sep_len] 
                       for i in range(0, len(input_val), sep_len)]
    
    # 使用指定的分隔符将分片后的字符串重新连接起来
    formatted_input = sep.join(formatted_input)
    
    return formatted_input[::-1]

def color(string, color):
    """
    功能：返回能打印对应颜色字符串的格式化后的字符串
    参数：
        string：需要被着色的字符串
        color：字符串对应的颜色，支持'black', 'red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'white'共8种颜色
    返回值：
        格式化后的字符串，可以使用 print(colorize_string('Hello, world!', 'red')) 来打印红色的 Hello, world!。
    """
    # ANSI转义码
    COLORS = {
        'black': '30',
        'red': '31',
        'green': '32',
        'yellow': '33',
        'blue': '34',
        'purple': '35',
        'cyan': '36',
        'white': '37'
    }

    # 判断有效颜色
    if color not in COLORS:
        return string

    # 格式化
    return '\033[{}m{}\033[0m'.format(COLORS[color], string)

def emph(text, bold=True, italic=False):
    """
    功能：将文本设置为斜体和/或加粗样式，并返回格式化后的字符串
    参数：
        text: 待格式化的文本
        bold: 是否设置加粗样式（默认为 True）
        italic: 是否设置斜体样式（默认为 False）
    返回值：
        返回格式化后的字符串
    """
    ATTRIBUTES = {
        'reset': '0',
        'bold': '1',
        'dim': '2',
        'italic': '3',
        'underlined': '4',
        'blink': '5',
        'reverse': '7',
        'hidden': '8'
    }

    attributes = []
    if bold:
        attributes.append('bold')
    if italic:
        attributes.append('italic')

    code = ';'.join([ATTRIBUTES[attr] for attr in attributes])
    if code:
        code = '\033[{}m'.format(code)

    return '{}{}{}\033[0m'.format(code, text, '\033[0m' if code else '')
