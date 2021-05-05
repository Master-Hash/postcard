from ipaddress import ip_address
from typing import Optional
from datetime import datetime

from fastapi import APIRouter, Depends, Header
from fastapi.requests import Request
from user_agents import parse
from babel.dates import format_date
from babel import Locale
from babel.support import Translations
from werkzeug.datastructures import LanguageAccept
from werkzeug.http import parse_accept_header
import pytz

from ..responses import SVGResponse
from ..dependencies import q
from ..templates import templates
from ..geoparse import getCity, getCityModel, getSpecialCity

router = APIRouter(
    tags=["postcards"],
    default_response_class=SVGResponse,
)


# 这里有一个奇怪的问题
# 理论上可以直接查到 locale
# 但是有时候地名查不到对应语言，所以必须处理下多语言情况？
# 先允许我在这里搞纯英文

# 有一个暂时的方案：把 accept-language 列表左右加长，
# 左边是 Query，右边是默认 en


@router.get(
    "/app",
    summary="动态电子名片",
)
async def postcard(
    request: Request,
    # 根据个人理解，
    # list, dict -> 请求体
    # 路径有的 -> 请求路径
    # 别的 -> 请求参数
    # 再别的就手写，Header 和 Cookie
    commons: q = Depends(),
    accept_language: Optional[str] = Header(None),
    user_agent: Optional[str] = Header(""),
):
    # 语言需要动态获取
    # 自己手动加 lang 和 tz 有点恼火……先咕掉？
    # 应该不用。

    langs = parse_accept_header(accept_language, LanguageAccept)
    # 优先级：Query > Header > Default
    lang = commons.lang or langs.best or "en"
    ip = ip_address(request.client.host)
    translation = Translations.load('locale', Locale.parse(lang, sep="-"))

    # 1.
    # 2. 特判 ip -> 返回 _()
    # 3. 查库
    # 4. 获取位置 -> 返回 GeoIP 译文
    # 5. 获取时区 -> 返回 str
    # 6. 时区 <- commons.tz or str or pytz.utc

    # is_global 并非保险箱……譬如 224.122.80.134 就查不到（
    model = getCityModel(ip)

    pos = model and getCity(model, lang=lang, langs=langs,
                            _=translation.gettext) \
        or getSpecialCity(ip, _=translation.gettext)

    # 时区优先级：
    # Query > Model > UTC
    tz = pytz.timezone(
        commons.tz
        or model and model.location.time_zone
        or "utc"
    )

    ua = parse(user_agent)
    date = format_date(
        datetime.now(tz=tz),
        format="full",
        locale=Locale.parse(lang, sep="-"),
    )

    # 其实不知道这么搞对不对……
    # 文档说了环境只能一开始初始化 env
    templates.env.install_gettext_translations(translation)

    items = commons.getSocial(request.query_params)

    return templates.TemplateResponse(
        "postcard.svg",
        {
            "request": request,
            "commons": commons,
            "pos": pos,
            "ua": ua,
            "date": date,
            "items": items,
            # tz 就不传进去了？
            # "gettext": translation.gettext,
        },
        media_type="image/svg+xml"
    )


@router.get(
    "/api",
    summary="旧版应用，因请求参数不兼容，可能将长期共存",
    deprecated=True,
)
async def api():
    '''
    请求参数参考[旧版项目 README](https://github.com/Master-Hash/postcard-legacy)
    '''
    ...
