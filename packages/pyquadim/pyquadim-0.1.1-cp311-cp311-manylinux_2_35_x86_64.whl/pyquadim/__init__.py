from . import pyquadim


def render(
        im: list[tuple[int]],
        width: int,
        height: int,
        ratio: tuple[int] = (1, 1),
        depth: int = 8,
        thres_ay: float = 20.,
        thres_cbcr: float = 2.,
        merge_method: str = "stdev",
        bg_color: str = "white",
        stroke_color: str = "black",
        stroke_width: int = 0,
        seed: int = 0,
        shape: str = "rect"
) -> list[tuple[int]]:
    """
    渲染，详细说明可以参考 https://github.com/eternal-io/quadim/blob/master/FULL-HELP.md
    :param im: 使用 Pillow 库读取图片，使用 Image.getdata() 将图片转换得到
    :param width: 图片的宽
    :param height: 图片的高
    :param ratio: 指定分割图片的程度
    :param depth: 四叉树的深度
    :param thres_ay: Alpha 和 Luma 通道的阈值，值越大，丢失的细节越多。
    :param thres_cbcr: 对其他两个色度通道进行处理阈值，值越大，丢失的细节越多。
    :param merge_method: 合并测试算法。["st-dev", "range"]
    :param bg_color: 背景颜色
    :param stroke_color: 边框颜色
    :param stroke_width: 边框宽度
    :param seed: 种子
    :param shape: 笔刷，目前有 ["rect", "circle", "cross", "yr-add", "yr-mul"]
    :return: 返回值使用 putdata() 转移回原图片上
    """

    return pyquadim.render(
        im,
        int(width),
        int(height),
        (int(ratio[0]), int(ratio[1])),
        int(depth),
        float(thres_ay),
        float(thres_cbcr),
        str(merge_method),
        str(bg_color),
        str(stroke_color),
        int(stroke_width),
        int(seed),
        str(shape)
    )
