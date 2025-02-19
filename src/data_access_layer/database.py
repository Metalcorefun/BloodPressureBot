from contextlib import asynccontextmanager
from typing import AsyncIterator

from alembic import command
from alembic.config import Config
from alembic.runtime import migration
from alembic.script import ScriptDirectory
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, AsyncConnection

from src.models.base import Base
from src.utils.config_reader import app_config
from src.utils.checkers import is_file_exists

engine = None
session_maker = None

async def initialize_db() -> None:
    global engine
    engine = create_async_engine(app_config.database_url_async)

    global session_maker
    session_maker = async_sessionmaker(engine, class_=AsyncSession,expire_on_commit=False)

    alembic_config = Config('alembic.ini')

    if not is_file_exists(app_config.database_file):
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
            await conn.run_sync(run_stamp, alembic_config)
    else:
        async with engine.begin() as conn:
            up_to_date = await conn.run_sync(check_current_head, alembic_config)
            if not up_to_date:
                await conn.run_sync(run_upgrade, alembic_config)

def check_current_head(connection: AsyncIterator[AsyncConnection], config: Config) -> bool:
    directory = ScriptDirectory.from_config(config)
    context = migration.MigrationContext.configure(connection)
    return context.get_current_revision() == directory.get_current_head()

def run_upgrade(connection, config):
    config.attributes['connection'] = connection
    command.upgrade(config, 'head')

def run_stamp(connection: AsyncIterator[AsyncConnection], config : Config) -> None:
    config.attributes['connection'] = connection
    command.stamp(config, 'head')

@asynccontextmanager
async def get_db_session() -> AsyncSession:
    session = None
    try:
        async with session_maker() as async_session:
            session = async_session
            yield session
    finally:
        await session.close()

async def commit_session():
    pass

async def execute_session():
    pass

async def refresh_session():
    pass


