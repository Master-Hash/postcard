from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter(
    tags=["redirections"],
    default_response_class=RedirectResponse,
)


@router.get(
    "/",
    summary="重定向至 Github 主页",
    status_code=301,
)
async def index():
    return RedirectResponse(
        "https://github.com/Master-Hash/postcard",
        status_code=301,
    )


@router.get(
    "/api",
    summary="重定向至 /app，当前 url 将弃用",
    deprecated=True,
    # responses=
    status_code=301,
)
async def api():
    return RedirectResponse(
        "/app",
        status_code=301,
    )
