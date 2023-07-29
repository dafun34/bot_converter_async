import sqlalchemy as sa

from tables.base import Base


class User(Base):
    __tablename__ = "users"
    id = sa.Column(sa.Integer, primary_key=True, index=True)
