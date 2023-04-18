import asyncio
import sys
from config import db
from alembic.config import Config
from alembic import command
from async_timeout import timeout
from loguru import logger

async def wait_for_db_conn(t: int = 15):
    logger.info(f'Waiting for the database to be up and ready [timeout={t}s]')
    res = False
    async with timeout(t):
        try:
            _, writer = await asyncio.open_connection(db.host, db.port)
            writer.close()
            await writer.wait_closed()
            res = True
        except ConnectionRefusedError as err:
            await asyncio.sleep(.1)
    if not res:
        logger.error('Database connection timed out')
        sys.exit(1)
    logger.info('Database connection was successfully established')

async def runmigrations():
    await wait_for_db_conn()
    alembic_cfg = Config('./alembic.ini')
    logger.info('Running migrations [upgrade head]')
    command.upgrade(alembic_cfg, "head")
    logger.info('Migrations were run successfully, the database should be up to date with the alembic head')
