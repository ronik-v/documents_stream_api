from uvicorn import run
from litestar import Litestar, get
from litestar.openapi import OpenAPIConfig

from src.config import settings


@get("/")
async def hello_world() -> str:
    return "Hello, World!"


if __name__ == "__main__":
    app = Litestar(route_handlers=[hello_world], openapi_config=OpenAPIConfig(title=settings.APP_NAME, version="1.0.0"))
    run(app, host=settings.APP_HOST, port=settings.APP_PORT)
