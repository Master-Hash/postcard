from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles

from .routers import redirections, postcard

app = FastAPI()
app.mount("/static", StaticFiles(directory="API/res"), name="static")

app.include_router(redirections.router)
app.include_router(postcard.router)


@app.get(
    "/teapot",
    status_code=418,
    tags=["test"],
)
async def egg():
    raise HTTPException(status_code=418)
