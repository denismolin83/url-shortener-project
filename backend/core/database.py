import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from typing import AsyncGenerator


DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql+asyncpg://user_name:supersecretpassword@localhost:5432/url_shortener_db")

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

Base = declarative_base()

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    session = AsyncSessionLocal()
    try:
        yield session
    finally:
        await session.close()
