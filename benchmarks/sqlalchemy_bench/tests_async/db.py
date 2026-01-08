import os
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
from sqlalchemy.pool import NullPool
from dotenv import load_dotenv


load_dotenv()
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_NAME = os.getenv("POSTGRES_DB")
DB_PORT = os.getenv("POSTGRES_PORT")


DATABASE_URL = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

DEBUG = "debug" if os.getenv("DEBUG") == "True" else False

POOL_SIZE = 25

engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=DEBUG,
    pool_size=POOL_SIZE,
    max_overflow=0,
    pool_timeout=30,
    pool_recycle=2500,
    pool_pre_ping=True,
)



AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session



#async def init_models():
#    async with engine.begin() as conn:
#        await conn.run_sync(Base.metadata.create_all)
