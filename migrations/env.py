from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
import asyncio

# Ваши модели
from app.models import Base
import fastapi_storages
from fastapi_storages.integrations.sqlalchemy import FileType

config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations():
    connectable = create_async_engine("postgresql+asyncpg://super_user:xDdmZeUxFYrlE83zbyBT7XH-hBSpNN07k6UjQicOejA@localhost:5432/office_db")
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

def run_migrations_online():
    asyncio.run(run_async_migrations())

run_migrations_online()