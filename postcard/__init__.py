from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles

from .routers import redirections, postcard

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
