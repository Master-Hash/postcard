import os
from dataclasses import dataclass
from enum import Enum
from typing import Optional

icons = [os.path.splitext(i)[0] for i in os.listdir("./API/res/icon")]


# 至于为什么要换名字…… in 作为关键字，不能是属性名
# 所以决定不重定向了，直接新开？
class Img(str, Enum):
    internal = "internal"
    external = "external"


@dataclass
class q:
    img: Optional[Img] = None
    src: Optional[str] = None
    # 试试使用 6 元矩阵代替各种缩放？
    # matrix: tuple[float]
    line: Optional[str] = None
    line2: Optional[str] = None
    # 我也没有更优雅的方案（
    for i in icons:
        exec(f"{i}: Optional[str] = None")
