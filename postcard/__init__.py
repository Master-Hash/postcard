from babel import Locale
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from werkzeug.datastructures import LanguageAccept
from werkzeug.http import parse_accept_header

from .routers import postcard, redirections
from .templates import getTranslation

tags_metadata = [
    {
        "name": "postcards",
        "description": "应用主体，返回 svg",
        "externalDocs": {
            "description": "Github 主页",
            "url": "https://github.com/Master-Hash/postcard",
        },
    },
    {
        "name": "redirections",
        "description": "重定向",
    },
    {
        "name": "test",
        "description": "I'm a Teapot.",
    },
]

app = FastAPI(
    openapi_tags=tags_metadata,
    title="动态电子名片",
    version="0.2.0",
)
app.mount("/static", StaticFiles(directory="API/res"), name="static")

app.include_router(redirections.router)
app.include_router(postcard.router)


@app.get(
    "/teapot",
    status_code=418,
    summary="彩蛋",
    tags=["test"],
)
async def egg():
    raise HTTPException(status_code=418)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    accept_language = request.headers.get("Accept-Language")
    langs = parse_accept_header(accept_language, LanguageAccept)
    lang = Locale.parse(langs.best, sep="-") or Locale.parse("en_US")
    translation = getTranslation(lang)
    _ = translation.gettext
    x: list[str] = []
    for i in exc.errors():
        p, param = i["loc"]
        if p == "query":
            p = _("Query parameter")
        x.append(_('%s %s is invaild') % (p, param))
    x.append(_('Please refer to Github, /docs or /redoc'))
    msg = "\\n".join(x)
    u = request.url.replace_query_params(
        quote=msg,
        github="Master-Hash/postcard",
        width=30 if lang.language == "zh" else 35,
        matrix_quote="(1 0 0 1 300 115)",
    )
    return RedirectResponse(
        f"{u.path}?{u.query}",
        status_code=307,
    )
