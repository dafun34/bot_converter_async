
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, \
    async_sessionmaker
from sqlalchemy.orm import sessionmaker

from config import settings


engine = create_async_engine(settings.DATABASE_URL, echo=True,)

async_session = async_sessionmaker(engine, expire_on_commit=False)
