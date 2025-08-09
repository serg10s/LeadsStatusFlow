from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base


SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./leads.db"
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
new_async_session = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


async def get_session():
    async with new_async_session() as session:
        yield session

Base = declarative_base()
