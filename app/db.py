from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from models import Base

async_engine = create_async_engine(
    url             =  DATABASE_URL,
    pool_size       =  15,
    max_overflow    =  5,
    echo_pool       =  True,
)


AsyncSessionLocal = sessionmaker(
    bind             = async_engine,
    class_           = AsyncSession,
    expire_on_commit = False,
)

# sqlalchemy_sessionmaker = async_sessionmaker(async_engine, expire_on_commit=False)
 
async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session