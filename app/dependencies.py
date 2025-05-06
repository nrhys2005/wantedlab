from app.db import AsyncSessionLocal


def get_async_db():
    async with AsyncSessionLocal() as session:
        async with session.begin():
            yield session


async def get_async_db_readonly():
    async with AsyncSessionLocal() as session:
        yield session