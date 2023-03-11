import sqlalchemy as sa
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(255))

