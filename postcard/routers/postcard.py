from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Header
from fastapi.requests import Request
from user_agents import parse
from babel.dates import format_date
from babel import Locale
from werkzeug.datastructures import LanguageAccept
from werkzeug.http import parse_accept_header
import pytz
from ..responses import SVGResponse
from ..dependencies import q
from ..templates import templates
from ..functions import getCity

router = APIRouter(
    tags=["postcards"],
    default_response_class=SVGResponse,
)


@router.get(
    "/app",
    summary="动态电子名片",
)
async def postcard(
    request: Request,
    commons: q = Depends(),
    accept_language: Optional[str] = Header(None),
    user_agent: Optional[str] = Header(""),
):
    locale = commons.lang or \
        parse_accept_header(accept_language, LanguageAccept) or \
        "en"
    geo = getCity(request.client.host, locale=locale)

    ua = parse(user_agent)
    date = format_date(
        datetime.now(tz=pytz.timezone(commons.tz)
                     if commons.tz else pytz.utc),
        format="full",
        locale=Locale.parse(locale, sep="-"),
    )

    return templates.TemplateResponse(
        "postcard.svg",
        {
            "request": request,
            "commons": commons,
            "geo": geo,
            "ua": ua,
            "date": date,
        },
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
