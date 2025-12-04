from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from collections.abc import Generator

from ..config import settings


class Base(DeclarativeBase, MappedAsDataclass):
    pass


DATABASE_URI = settings.POSTGRES_URI
DATABASE_PREFIX = settings.POSTGRES_SYNC_PREFIX
DATABASE_URL = f"{DATABASE_PREFIX}{DATABASE_URI}"


# async_engine = create_async_engine(DATABASE_URL, echo=False, future=True)

# local_session = async_sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)


# async def async_get_db() -> AsyncGenerator[AsyncSession, None]:
#     async with local_session() as db:
#         yield db

engine = create_engine(DATABASE_URL, echo=False, future=True)

# Tạo Session factory
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Sync get_db
def get_db() -> Generator:
    """
    Sync generator cho DB session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()