from uvicorn import run
from litestar import Litestar, Response
from litestar.openapi import OpenAPIConfig

from src.config import settings
from src.docs.routers import DocumentsController


if __name__ == "__main__":
    app = Litestar(
        route_handlers=[DocumentsController],
        openapi_config=OpenAPIConfig(title=settings.APP_NAME, version="1.0.0"),
        debug=True,
    )

    run(app, host=settings.APP_HOST, port=settings.APP_PORT)
