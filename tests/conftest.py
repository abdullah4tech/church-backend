import pytest
from typing import AsyncGenerator
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base import Base
from app.db.session import get_db

# Use an in-memory SQLite database for testing if possible, 
# or mock the session. Since we use asyncpg, sqlite might not work directly 
# without aiosqlite. For this basic test, we'll try to mock the DB dependency 
# or just test endpoints that don't require DB (like root).

@pytest.fixture
async def client() -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c
