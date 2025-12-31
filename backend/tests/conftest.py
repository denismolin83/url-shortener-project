import asyncio
from contextlib import asynccontextmanager
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from main import app
from core.database import DATABASE_URL, Base, get_db_session
import pytest_asyncio


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def db_session():
    engine_test = create_async_engine(url=DATABASE_URL, future=True)
    AsyncSessionTest = async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)


    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionTest() as session:
        yield session
        await session.rollback()

    
    #async with engine_test.begin() as conn:
        #await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def client(db_session: AsyncSession):
    async def _override_get_db_session():
        yield db_session
    
    app.dependency_overrides[get_db_session] = _override_get_db_session
    
    from httpx import AsyncClient, ASGITransport
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac  
    
    app.dependency_overrides.clear()