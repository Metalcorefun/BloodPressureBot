from contextlib import asynccontextmanager
from typing import AsyncIterator
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, AsyncConnection

from src.models.base import Base

from src.utils.config_reader import app_config

engine = None
session_maker = None

#TODO: maybe shoud use Alembic for schema mighrations
async def initialize_db():
    global engine
    engine = create_async_engine(app_config.database_url_async)

    global session_maker
    session_maker = async_sessionmaker(engine, class_=AsyncSession,expire_on_commit=False)

    if not await all_tables_exists(get_db_session()):
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

@asynccontextmanager
async def get_db_session() -> AsyncSession:
    session = None
    try:
        async with session_maker() as async_session:
            session = async_session
            yield session
    finally:
        await session.close()

def inspect_tables(conn: AsyncIterator[AsyncConnection]):
    inspector = inspect(conn)
    return inspector.get_table_names()

#TODO: refactor for alembic execution
async def all_tables_exists(session: AsyncSession) -> bool:
    tbls = Base.metadata.tables.values()
    schema_tables = [table.name for table in Base.metadata.tables.values()]

    db_tables = []
    async with engine.begin() as conn:
        db_tables = await conn.run_sync(inspect_tables)

    if set(schema_tables) != set(db_tables):
        return False
    return True

async def commit_session():
    pass

async def execute_session():
    pass

async def refresh_session():
    pass


