from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .exceptions import ApplicationException, application_exception_handler
from .containers import Container
from .auto_config import ApplicationAutoConfig
from prometheus_fastapi_instrumentator import Instrumentator

import config


async def create_app():
    container = Container()
    app_config = ApplicationAutoConfig('.modules')
    app_config.wire_submodules(container)

    db = container.db()
    app = FastAPI()

    for router in app_config.get_routers():
        app.include_router(router, prefix='/api')

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )

    app.add_event_handler('startup', db.on_startup)
    app.add_exception_handler(ApplicationException, application_exception_handler)
    app.container = container

    Instrumentator().instrument(app).expose(app)

    return app
