import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve
from watchfiles import run_process
from .app import create_app
from .runmigrations import runmigrations
from .custom_logging import create_logger
import config as application_config


def runserver():
    logger = create_logger('./logging_config.yml')
    asyncio.run(runmigrations())
    config = Config()
    config.bind = [f'{application_config.hypercorn.bind_ip}:{application_config.hypercorn.bind_port}']
    app = asyncio.run(create_app())
    asyncio.run(serve(app, config))


if __name__ == '__main__':
    run_process('./', target=runserver)
