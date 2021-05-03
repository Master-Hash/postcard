# from typing import Any
from fastapi import APIRouter, Depends
from fastapi.requests import Request
# from fastapi.responses import HTMLResponse
from ..responses import SVGResponse
from ..dependencies import q
from ..templates import templates

router = APIRouter(
    tags=["postcard"],
    default_response_class=SVGResponse,
)


@router.get(
    "/app",
    summary="动态电子名片"
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


# @router.get(
#     "/jinja",
#     response_class=HTMLResponse,
# )
# async def jinja(
#     request: Request,
# ):
#     return templates.TemplateResponse(
#         "play.html",
#         {
#             "request": request,
#         },
#     )
