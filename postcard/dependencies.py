import os
from dataclasses import dataclass
from enum import Enum
from functools import reduce
from operator import add
from textwrap import wrap
from typing import Any, Optional

from babel import localedata, Locale
from pytz import common_timezones

icons = [os.path.splitext(i)[0] for i in os.listdir("./API/res/icon")]


def concat(ll: list[list[Any]]) -> list[Any]:
    return reduce(add, ll)

# 至于为什么要换名字…… in 作为关键字，不能是属性名
# 所以决定不重定向了，直接新开？
# class Img(str, Enum):
#     internal = "internal"
#     external = "external"


TimeZone = Enum("Timezone", {i: i for i in common_timezones}, type=str)
Language = Enum("Language",
                {i: i for i in localedata.locale_identifiers()}, type=str)


@dataclass
class q:
    # 不想搞图片了（
    # 我又不擅长找图，画图，赏图（
    # img: Optional[Img] = None
    # src: Optional[str] = None
    # 试试使用 6 元矩阵代替各种缩放？
    # matrix: tuple[float]
    matrix_detail: Optional[str] = '(1 0 0 1 25 35)'
    matrix_line: Optional[str] = '(1 0 0 1 0 0)'
    matrix_contact: Optional[str] = '(1 0 0 1 300 15)'
    matrix_quote: Optional[str] = '(1 0 0 1 300 100)'
    quote: str = ""
    lang: Optional[Language] = None
    tz: Optional[TimeZone] = None
    width: int = 30
    # 我也没有更优雅的方案（
    for i in icons:
        exec(f"{i}: Optional[str] = None")
    else:
        del i

    @staticmethod
    def getSocial(query_params) -> list[str]:
        return {i: query_params[i] for i in query_params if i in icons}

    def __post_init__(self):
        self.quoteLines = self.getQuote()
        self.locale = self.lang and Locale(self.lang)

    def getQuote(self) -> list[str]:
        ll = self.quote.split("\\n")
        return concat([
            wrap(
                i,
                width=self.width,
            ) for i in ll
        ])
