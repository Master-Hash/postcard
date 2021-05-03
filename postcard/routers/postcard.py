# from typing import Any
from fastapi import APIRouter, Depends
from fastapi.requests import Request
# from fastapi.responses import HTMLResponse
from ..responses import SVGResponse
from ..dependencies import q
from ..templates import templates

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
):
    return templates.TemplateResponse(
        "postcard.svg",
        {
            "request": request,
            "commons": commons,
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
