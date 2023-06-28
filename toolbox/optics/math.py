import math

def calc_resolution(d, f, R):
    """
    计算给定距离下镜头的分辨率。

    参数:
    d (float): 目标距离，单位为米。
    f (float): 镜头焦距，单位为毫米。
    R (float): 镜头角分辨率，单位为MIL。

    返回值:
    float: 给定距离下镜头的分辨率，单位为像素/米。
    """
    # 将MIL转换为弧度
    R = math.radians(R / 1000)
    
    # 计算相应距离下的镜头分辨率
    P = (2 * d * math.tan(R/2)) / f
    
    return P