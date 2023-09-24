import sqlalchemy as sa

from tables.base import Base


class User(Base):
    __tablename__ = "users"
    id = sa.Column(sa.BigInteger, primary_key=True, index=True)
    is_admin = sa.Column(sa.Boolean)
